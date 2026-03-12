# 🌱 Plant Shop - Website Bán Cây Cảnh & Tư Vấn AI

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com/)

Chào mừng đến với **Plant Shop** - Nền tảng thương mại điện tử chuyên cung cấp các loại cây cảnh mini, tích hợp trợ lý ảo AI thông minh giúp tư vấn và chăm sóc cây trồng.

## 🚀 Tính Năng Nổi Bật

### 🛒 Dành Cho Khách Hàng (Customer)
- **Mua sắm trực tuyến:** Duyệt danh mục cây, tìm kiếm, lọc theo nhiều tiêu chí (ánh sáng, độ khó, giá).
- **Trợ lý ảo AI (Chatbot):** 
  - Chat trực tiếp để hỏi về cách chăm sóc cây.
  - Tư vấn chọn cây phù hợp với không gian sống.
  - Nhận diện nhu cầu qua ngôn ngữ tự nhiên.
- **Quản lý đơn hàng:** Theo dõi trạng thái đơn hàng, lịch sử mua sắm.
- **Đánh giá & Bình luận:** Review sản phẩm 5 sao kèm bình luận chi tiết.

### 🛠 Dành Cho Quản Trị Viên (Admin)
- **Dashboard:** Thống kê doanh thu, số lượng đơn hàng.
- **Quản lý sản phẩm:** Thêm/Sửa/Xóa cây cảnh, cập nhật tồn kho.
- **Quản lý đơn hàng:** Duyệt đơn, cập nhật trạng thái vận chuyển.
- **Quản lý Chatbot:** Cấu hình từ khóa và kịch bản trả lời cho AI.

## 📂 Cấu Trúc Dự Án

```
plant_shop_website/
├── manage.py                   # Django management script
├── requirements.txt            # Danh sách thư viện
├── readme.md                   # Tài liệu dự án
├── db.sqlite3                  # Database (SQLite)
│
├── plant_shop/                 # Project Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── products/                   # Quản lý Sản phẩm & Danh mục
├── orders/                     # Quản lý Giỏ hàng & Đơn hàng
├── users/                      # Quản lý Tài khoản (Auth)
├── reviews/                    # Đánh giá & Bình luận
├── plant_recommendation/       # Hệ thống AI Chatbot (NLP + Decision Tree)
│
├── templates/                  # Giao diện HTML (Bootstrap 5)
├── static/                     # CSS, JS, Images
├── media/                      # File upload (Ảnh sản phẩm, Avatar)
│
└── scripts/                    # Scripts tiện ích (Data import, Training)
```

## 📦 Cài Đặt & Chạy Dự Án

### 1. Clone dự án
```bash
git clone https://github.com/tuanlamviec007/plant_shop_website.git
cd plant_shop_website
```

### 2. Thiết lập môi trường ảo (Virtual Env)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# MacOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Khởi tạo Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo tài khoản Admin
```bash
python manage.py createsuperuser
```

### 6. Chạy Server
```bash
python manage.py runserver
```
Truy cập: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 👥 Thành Viên Nhóm 5
1. **Nguyễn Đắc Tuấn** - Developer
2. **Đàm Trường Vũ** - Developer
3. **Nguyễn Thị Mai Anh** - Báo cáo 

---
*Dự án phục vụ mục đích học tập.*