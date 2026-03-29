"""
Admin Dashboard - Statistics View
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import json

from orders.models import Order, OrderItem
from products.models import Product, Category
from reviews.models import Review


@staff_member_required
def admin_dashboard(request):
    now = timezone.now()
    today = now.date()
    
    # ── Khoảng thời gian ──
    this_month_start = today.replace(day=1)
    last_month_end   = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    this_week_start  = today - timedelta(days=today.weekday())
    yesterday        = today - timedelta(days=1)

    # ─────────────────────────────────────────────
    # KPI CARDS
    # ─────────────────────────────────────────────
    # Tổng doanh thu (đã giao)
    delivered_orders = Order.objects.filter(status__in=['delivered', 'confirmed'])
    total_revenue    = delivered_orders.aggregate(s=Sum('total_amount'))['s'] or 0

    # Doanh thu tháng này
    revenue_this_month = delivered_orders.filter(
        created_at__date__gte=this_month_start
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    # Doanh thu tháng trước
    revenue_last_month = delivered_orders.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).aggregate(s=Sum('total_amount'))['s'] or 0

    # Tăng trưởng doanh thu
    if revenue_last_month > 0:
        revenue_growth = round((revenue_this_month - revenue_last_month) / revenue_last_month * 100, 1)
    else:
        revenue_growth = 100.0 if revenue_this_month > 0 else 0.0

    # Tổng đơn hàng
    total_orders      = Order.objects.count()
    orders_this_month = Order.objects.filter(created_at__date__gte=this_month_start).count()
    orders_today      = Order.objects.filter(created_at__date=today).count()

    # Đơn hàng theo trạng thái
    order_status_counts = {
        'pending':   Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'shipping':  Order.objects.filter(status='shipping').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }

    # Người dùng
    total_users    = User.objects.count()
    new_users_week = User.objects.filter(date_joined__date__gte=this_week_start).count()

    # Sản phẩm
    total_products  = Product.objects.filter(is_active=True).count()
    low_stock_count = Product.objects.filter(is_active=True, stock__lte=5).count()

    # ─────────────────────────────────────────────
    # DOANH THU 12 THÁNG GẦN NHẤT (cho biểu đồ)
    # ─────────────────────────────────────────────
    twelve_months_ago = today.replace(day=1) - timedelta(days=365)
    monthly_revenue_qs = (
        Order.objects
        .filter(status__in=['delivered', 'confirmed'], created_at__date__gte=twelve_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(revenue=Sum('total_amount'), count=Count('id'))
        .order_by('month')
    )

    # Build full 12-month list (fill 0 for missing months)
    months_labels  = []
    months_revenue = []
    months_orders  = []

    month_data_map = {
        item['month'].strftime('%Y-%m'): item
        for item in monthly_revenue_qs
    }

    for i in range(11, -1, -1):
        # Go back `i` months
        if now.month - i <= 0:
            m = now.month - i + 12
            y = now.year - 1
        else:
            m = now.month - i
            y = now.year
        key = f'{y}-{m:02d}'
        MONTH_NAMES = ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12']
        months_labels.append(f'{MONTH_NAMES[m-1]}/{str(y)[2:]}')
        if key in month_data_map:
            months_revenue.append(float(month_data_map[key]['revenue']))
            months_orders.append(month_data_map[key]['count'])
        else:
            months_revenue.append(0)
            months_orders.append(0)

    # ─────────────────────────────────────────────
    # DOANH THU 30 NGÀY GẦN NHẤT (cho biểu đồ line)
    # ─────────────────────────────────────────────
    thirty_days_ago = today - timedelta(days=29)
    daily_revenue_qs = (
        Order.objects
        .filter(status__in=['delivered', 'confirmed'], created_at__date__gte=thirty_days_ago)
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(revenue=Sum('total_amount'), count=Count('id'))
        .order_by('day')
    )
    daily_data_map = {
        item['day'].strftime('%Y-%m-%d'): item
        for item in daily_revenue_qs
    }
    days_labels  = []
    days_revenue = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        days_labels.append(f'{d.day}/{d.month}')
        key = d.strftime('%Y-%m-%d')
        days_revenue.append(float(daily_data_map[key]['revenue']) if key in daily_data_map else 0)

    # ─────────────────────────────────────────────
    # TOP 5 SẢN PHẨM BÁN CHẠY
    # ─────────────────────────────────────────────
    top_products = (
        OrderItem.objects
        .values('product__name', 'product__id')
        .annotate(total_sold=Sum('quantity'), total_revenue=Sum('subtotal'))
        .order_by('-total_sold')[:5]
    )

    # ─────────────────────────────────────────────
    # 10 ĐƠN HÀNG GẦN NHẤT
    # ─────────────────────────────────────────────
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # ─────────────────────────────────────────────
    # SẢN PHẨM SẮP HẾT HÀNG
    # ─────────────────────────────────────────────
    low_stock_products = Product.objects.filter(is_active=True, stock__lte=10).order_by('stock')[:8]

    # ─────────────────────────────────────────────
    # ĐÁNH GIÁ & REVIEW
    # ─────────────────────────────────────────────
    try:
        total_reviews    = Review.objects.count()
        avg_rating       = Review.objects.aggregate(a=Avg('rating'))['a'] or 0
        reviews_this_month = Review.objects.filter(created_at__date__gte=this_month_start).count()
    except Exception:
        total_reviews    = 0
        avg_rating       = 0
        reviews_this_month = 0

    # ─────────────────────────────────────────────
    # PHÂN BỔ DANH MỤC (cho pie chart)
    # ─────────────────────────────────────────────
    category_sales = (
        OrderItem.objects
        .values('product__category__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:6]
    )
    cat_labels  = [c['product__category__name'] or 'Khác' for c in category_sales]
    cat_values  = [c['total_sold'] or 0 for c in category_sales]

    context = {
        # KPIs
        'total_revenue':        total_revenue,
        'revenue_this_month':   revenue_this_month,
        'revenue_last_month':   revenue_last_month,
        'revenue_growth':       revenue_growth,
        'total_orders':         total_orders,
        'orders_this_month':    orders_this_month,
        'orders_today':         orders_today,
        'order_status_counts':  order_status_counts,
        'total_users':          total_users,
        'new_users_week':       new_users_week,
        'total_products':       total_products,
        'low_stock_count':      low_stock_count,
        'total_reviews':        total_reviews,
        'avg_rating':           round(avg_rating, 1),
        'reviews_this_month':   reviews_this_month,

        # Charts (JSON)
        'months_labels':        json.dumps(months_labels),
        'months_revenue':       json.dumps(months_revenue),
        'months_orders':        json.dumps(months_orders),
        'days_labels':          json.dumps(days_labels),
        'days_revenue':         json.dumps(days_revenue),
        'cat_labels':           json.dumps(cat_labels),
        'cat_values':           json.dumps(cat_values),

        # Tables
        'top_products':         top_products,
        'recent_orders':        recent_orders,
        'low_stock_products':   low_stock_products,

        # Meta
        'today':                today,
        'title':                'Dashboard Thống Kê',
    }

    return render(request, 'admin/custom_dashboard.html', context)
