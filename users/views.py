# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile


def register_view(request):
    """Đăng ký tài khoản"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        # Validate
        if not all([username, email, password, password2]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return render(request, 'users/register.html')

        if password != password2:
            messages.error(request, 'Mật khẩu không khớp!')
            return render(request, 'users/register.html')

        if len(password) < 8:
            messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự!')
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại!')
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng!')
            return render(request, 'users/register.html')

        # Tạo user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Tạo profile
            UserProfile.objects.create(
                user=user,
                phone=phone,
                address=address
            )

            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            return render(request, 'users/register.html')

    return render(request, 'users/register.html')


def login_view(request):
    """Đăng nhập"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}!')

            # Redirect đến trang trước đó hoặc home
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')

    return render(request, 'users/login.html')


def logout_view(request):
    """Đăng xuất"""
    logout(request)
    messages.success(request, 'Đã đăng xuất!')
    return redirect('home')


@login_required
def profile_view(request):
    """Xem và chỉnh sửa hồ sơ"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Cập nhật thông tin User
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        # Cập nhật profile
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')

        # Upload avatar
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        profile.save()

        messages.success(request, 'Cập nhật hồ sơ thành công!')
        return redirect('profile')

    # Thống kê user
    from orders.models import Order
    total_orders = Order.objects.filter(user=request.user).count()
    completed_orders = Order.objects.filter(user=request.user, status='delivered').count()

    context = {
        'profile': profile,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'users/profile.html', context)


# products/context_processors.py
from orders.models import Cart


def cart_count(request):
    """Context processor để hiển thị số lượng giỏ hàng ở navbar"""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
        return {'cart_count': count}
    return {'cart_count': 0}


def categories(request):
    """Context processor để hiển thị categories ở mọi trang"""
    from products.models import Category
    return {
        'all_categories': Category.objects.filter(is_active=True)
    }


from django.shortcuts import render

# Create your views here.
