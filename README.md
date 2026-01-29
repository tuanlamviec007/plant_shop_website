# 🌱 PLANT SHOP - Website Bán Cây Cảnh Mini với AI

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com/)

Website thương mại điện tử bán cây cảnh mini tích hợp tính năng AI nhận diện cây qua hình ảnh.

## 📋 Mục Tiêu Dự Án

Xây dựng hệ thống website hoàn chỉnh cho phép:
- Người dùng mua bán cây cảnh mini trực tuyến
- Sử dụng AI để nhận diện loại cây từ hình ảnh
- Quản lý đơn hàng, sản phẩm, khách hàng
- Thống kê doanh thu và báo cáo

## 🎯 Tính Năng Chính

### Cho Khách Hàng (User)
- ✅ Đăng ký, đăng nhập, quản lý hồ sơ
- ✅ Xem danh sách sản phẩm (phân trang, tìm kiếm, lọc, sắp xếp)
- ✅ Xem chi tiết sản phẩm, hướng dẫn chăm sóc
- ✅ Thêm vào giỏ hàng, đặt hàng
- ✅ Theo dõi trạng thái đơn hàng
- ✅ Đánh giá, bình luận sản phẩm
- ✅ Nhận diện cây qua AI (upload/chụp ảnh)

### Cho Quản Trị Viên (Admin)
- ✅ Quản lý sản phẩm (CRUD)
- ✅ Quản lý danh mục cây cảnh
- ✅ Quản lý đơn hàng (duyệt, cập nhật trạng thái)
- ✅ Quản lý người dùng
- ✅ Xem thống kê, báo cáo
- ✅ Quản lý bình luận, đánh giá

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Python:** 3.13
- **Framework:** Django 5.0.1
- **Database:** SQLite3 (development), PostgreSQL (production)
- **ORM:** Django ORM

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5.3**
- **Font Awesome 6.4**
- **Chart.js** (thống kê)

### AI
- **TensorFlow/Keras** hoặc **Plant.id API**

## 📦 Cài Đặt và Chạy Dự Án

### Yêu Cầu Hệ Thống
- Python 3.13+
- PyCharm 2025.3.1 (recommended)
- pip (Python package manager)

### Bước 1: Clone dự án
```bash
git clone https://github.com/your-username/plant-shop.git
cd plant-shop
```

### Bước 2: Tạo Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# MacOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cấu hình Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 5: Tạo dữ liệu mẫu
```bash
python manage.py seed_data
```

### Bước 6: Tạo Superuser (Admin)
```bash
python manage.py createsuperuser

# Nhập thông tin:
Username: admin
Email: admin@plantshop.com
Password: Admin@123
```

### Bước 7: Chạy Server
```bash
python manage.py runserver
```

Truy cập: **http://127.0.0.1:8000/**

## 👤 Tài Khoản Mẫu

### Admin
- **Username:** admin
- **Password:** Admin@123
- **URL:** http://127.0.0.1:8000/admin/

### User
- **Username:** user1
- **Password:** User@123

---

## 📂 Cấu Trúc Thư Mục

```
plant_shop/
├── manage.py                   # Django management script
├── requirements.txt            # Thư viện Python
├── README.md                   # File này
├── db.sqlite3                  # Database
│
├── plant_shop/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── products/                   # App Sản phẩm
│   ├── models.py              # Category, Product
│   ├── views.py               # Logic xử lý
│   ├── urls.py                # URL routing
│   └── admin.py               # Django admin
│
├── orders/                     # App Đơn hàng
│   ├── models.py              # Cart, Order, OrderItem
│   ├── views.py
│   └── urls.py
│
├── users/                      # App Người dùng
│   ├── models.py              # UserProfile
│   ├── views.py               # Login, Register
│   └── urls.py
│
├── reviews/                    # App Đánh giá
│   ├── models.py              # Review
│   └── views.py
│
├── ai_recognition/             # App AI Nhận diện
│   ├── models.py              # PlantRecognition
│   └── views.py
│
├── templates/                  # HTML templates
│   ├── base.html              # Layout chung
│   ├── home.html              # Trang chủ
│   ├── products/
│   ├── orders/
│   └── users/
│
├── static/                     # Static files
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/                      # User uploads
    ├── products/
    ├── plants/
    └── avatars/
```

## 🗄️ Cơ Sở Dữ Liệu

### Các Bảng Chính
1. **users** - Người dùng
2. **user_profiles** - Hồ sơ người dùng
3. **categories** - Danh mục cây
4. **products** - Sản phẩm
5. **cart** - Giỏ hàng
6. **orders** - Đơn hàng
7. **order_items** - Chi tiết đơn hàng
8. **reviews** - Đánh giá
9. **plant_recognitions** - Lịch sử AI

### Quan Hệ
- User 1-n Order
- Order 1-n OrderItem
- Product 1-n OrderItem
- Category 1-n Product
- User 1-n Review
- Product 1-n Review

## 🚀 Tính Năng Nổi Bật

### 1. Tìm Kiếm & Lọc Thông Minh
- Tìm kiếm theo tên sản phẩm
- Lọc theo danh mục, giá, độ khó chăm sóc
- Sắp xếp theo giá, đánh giá, bán chạy

### 2. Giỏ Hàng Linh Hoạt
- Thêm/Xóa/Cập nhật số lượng
- Tính tổng tiền tự động
- Kiểm tra tồn kho real-time

### 3. Quản Lý Đơn Hàng
- Trạng thái: Pending → Confirmed → Shipping → Delivered
- Cho phép hủy đơn (khi Pending)
- Tự động giảm stock khi xác nhận

### 4. AI Nhận Diện Cây (Coming Soon)
- Upload hoặc chụp ảnh
- Nhận diện loại cây
- Gợi ý sản phẩm tương tự

### 5. Đánh Giá & Xếp Hạng
- Chỉ cho phép user đã mua đánh giá
- Cập nhật rating tự động
- Admin kiểm duyệt bình luận

## 📊 Tiến Độ Dự Án

### ✅ Đã Hoàn Thành (Kỹ Năng 1 & 2)
- [x] Phân tích và thiết kế hệ thống
- [x] Thiết kế ERD, Use Case
- [x] Tạo Models (8 bảng)
- [x] Cấu hình Django Admin
- [x] Tạo dữ liệu mẫu
- [x] Giao diện Home, Products
- [x] Đăng nhập, Đăng ký
- [x] Giỏ hàng, Checkout
- [x] Responsive design

### 🔄 Đang Thực Hiện (Kỹ Năng 3)
- [ ] Hoàn thiện CRUD đầy đủ
- [ ] Tính năng AI nhận diện
- [ ] Upload ảnh sản phẩm
- [ ] Chi tiết đơn hàng
- [ ] Thống kê Dashboard

### 📅 Kế Hoạch (Kỹ Năng 4)
- [ ] Chart.js biểu đồ
- [ ] Bảo mật nâng cao
- [ ] Tối ưu hiệu năng
- [ ] Viết báo cáo
- [ ] Video demo

## 🧪 Testing

### Test thủ công
```bash
# Chạy từng chức năng và kiểm tra
1. Đăng ký user mới
2. Đăng nhập
3. Xem sản phẩm
4. Thêm vào giỏ hàng
5. Đặt hàng
6. Admin duyệt đơn
7. User đánh giá
```

### Unit test (Coming Soon)
```bash
python manage.py test
```

## 🐛 Troubleshooting

### Lỗi "No module named 'django'"
```bash
pip install Django==5.0.1
```

### Lỗi migrate
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Lỗi static files
```bash
python manage.py collectstatic
```

## 📝 Ghi Chú Phát Triển

### Git Workflow
```bash
# Commit thường xuyên
git add .
git commit -m "feat: thêm chức năng đăng nhập"
git push origin main
```

### Code Style
- Sử dụng PEP 8 cho Python
- Comment code rõ ràng
- Đặt tên biến có ý nghĩa

## 👥 Thành Viên Nhóm

1. **Nguyễn Đắc Tuấn** - Backend Developer
2. **Đàm Trường Vũ** - Frontend Developer  
3. **Nguyễn Thị Mai Anh** - AI Integration & Testing

## 📞 Liên Hệ

- **Email:** info@plantshop.com
- **GitHub:** https://github.com/Tuan/plant-shop

---

## 📜 License

Dự án này được phát triển cho mục đích học tập.

**© 2026 Plant Shop - Nhóm 5python manage.py runserver**