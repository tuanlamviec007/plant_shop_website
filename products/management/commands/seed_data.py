from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from orders.models import Order, OrderItem, Cart
from reviews.models import Review
from users.models import UserProfile
from django.utils.text import slugify
from django.core.files.base import ContentFile
import random

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho website'


    def handle(self, *args, **kwargs):
        from django.conf import settings
        import os
        from django.core.files import File

        self.stdout.write('Deleting old data...')
        Order.objects.all().delete()
        Cart.objects.all().delete()
        Review.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        
        # 1. Tạo Users
        self.stdout.write('Creating Users...')
        # Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@plantshop.com', 'Admin@123')
            self.stdout.write('- Admin user created (admin/Admin@123)')
        
        # Normal User
        user1 = User.objects.create_user('user1', 'user1@example.com', 'User@123', first_name='Nguyen', last_name='A')
        UserProfile.objects.create(user=user1, phone='0987654321', address='123 Duong Le Loi, TP.HCM')
        self.stdout.write('- Normal user created (user1/User@123)')

        # 2. Tạo Categories
        self.stdout.write('Creating Categories...')
        categories = [
            {'name': 'Sen đá', 'desc': 'Các loại sen đá để bàn, dễ chăm sóc.'},
            {'name': 'Xương rồng', 'desc': 'Cây chịu hạn tốt, hình dáng độc đáo.'},
            {'name': 'Cây để bàn', 'desc': 'Cây nhỏ gọn, thanh lọc không khí.'},
            {'name': 'Bonsai Mini', 'desc': 'Cây dáng thế nghệ thuật kích thước nhỏ.'},
            {'name': 'Terrarium', 'desc': 'Hệ sinh thái thu nhỏ trong bình thủy tinh.'},
        ]
        
        cats = []
        for c in categories:
            cat = Category.objects.create(name=c['name'], description=c['desc'])
            cats.append(cat)

        # 3. Tạo Products
        self.stdout.write('Creating Products...')
        products_data = [
            # Sen đá
            {'name': 'Sen đá Kim Cương', 'price': 50000, 'cat': 0, 'care': 'easy'},
            {'name': 'Sen đá Nâu', 'price': 35000, 'cat': 0, 'care': 'easy'},
            {'name': 'Sen đá Phật Bà', 'price': 120000, 'cat': 0, 'care': 'medium'},
            
            # Xương rồng
            {'name': 'Xương rồng Tai Thỏ', 'price': 45000, 'cat': 1, 'care': 'easy'},
            {'name': 'Xương rồng Bát Tiên', 'price': 80000, 'cat': 1, 'care': 'medium'},
            
            # Cây để bàn
            {'name': 'Cây Kim Tiền', 'price': 150000, 'cat': 2, 'care': 'easy'},
            {'name': 'Cây Lưỡi Hổ', 'price': 90000, 'cat': 2, 'care': 'easy'},
            {'name': 'Cây Trầu Bà Đế Vương', 'price': 200000, 'cat': 2, 'care': 'medium'},
            
            # Bonsai
            {'name': 'Tùng La Hán Mini', 'price': 450000, 'cat': 3, 'care': 'hard'},
            {'name': 'Sung My Mini', 'price': 350000, 'cat': 3, 'care': 'medium'},
            
            # Terrarium
            {'name': 'Terrarium Rừng Nhiệt Đới', 'price': 550000, 'cat': 4, 'care': 'medium'},
            {'name': 'Terrarium Sa Mạc', 'price': 400000, 'cat': 4, 'care': 'easy'},
        ]
        
        products = []
        for p in products_data:
            # Check for local image in static/images
            image_name = p['name'] + '.jpg'
            # Special case for case-insensitive match if needed, but let's try direct first
            if p['name'] == 'Terrarium Sa Mạc':
                image_name = 'terrarium sa mạc.jpg'

            static_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_name)
            
            if os.path.exists(static_image_path):
                with open(static_image_path, 'rb') as f:
                    prod = Product.objects.create(
                        category=cats[p['cat']],
                        name=p['name'],
                        description=f"Mô tả chi tiết cho {p['name']}. Cây khỏe mạnh, được tuyển chọn kỹ.",
                        price=p['price'],
                        original_price=p['price'] * 1.2,
                        stock=random.randint(5, 50),
                        care_level=p['care'],
                        is_featured=random.choice([True, False]),
                    )
                    prod.image.save(image_name, File(f), save=True)
            else:
                 prod = Product.objects.create(
                    category=cats[p['cat']],
                    name=p['name'],
                    description=f"Mô tả chi tiết cho {p['name']}. Cây khỏe mạnh, được tuyển chọn kỹ.",
                    price=p['price'],
                    original_price=p['price'] * 1.2,
                    stock=random.randint(5, 50),
                    care_level=p['care'],
                    is_featured=random.choice([True, False]),
                    image='products/default_plant.jpg' 
                )
            
            products.append(prod)

        # 4. Tạo Orders & Reviews
        self.stdout.write('Creating Sample Orders...')
        
        # Order 1: Completed
        order1 = Order.objects.create(
            user=user1,
            total_amount=0, # Auto triggers save logic but we set explicitly later
            customer_name='Nguyen Van A',
            customer_phone='0987654321',
            shipping_address='Hanoi',
            status='delivered'
        )
        
        # Items
        item1 = OrderItem.objects.create(
            order=order1,
            product=products[0],
            product_name=products[0].name,
            quantity=2,
            price=products[0].price,
            subtotal=products[0].price * 2
        )
        order1.total_amount = item1.subtotal
        order1.save()
        
        # Review for product 0
        Review.objects.create(
            user=user1,
            product=products[0],
            rating=5,
            comment='Cay dep, dong goi ky!',
            is_approved=True
        )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
