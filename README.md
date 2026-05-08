# 🌱 Plant Shop - Website Bán Cây Cảnh & Tư Vấn AI

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)](https://getbootstrap.com/)
[![AI](https://img.shields.io/badge/AI-Gemini%20RAG-orange)](https://ai.google.dev/)

Website thương mại điện tử chuyên cung cấp cây cảnh mini, tích hợp trợ lý ảo AI thông minh giúp tư vấn và chăm sóc cây trồng.

---

## 🚀 Tính Năng Nổi Bật

### 🛒 Dành Cho Khách Hàng
- **Mua sắm trực tuyến:** Duyệt danh mục cây, tìm kiếm, lọc theo ánh sáng / độ khó / giá
- **Trợ lý ảo AI (Chatbot):**
  - Chat trực tiếp hỏi về cách chăm sóc cây
  - Tư vấn chọn cây phù hợp không gian sống
  - So sánh 2 loại cây cùng lúc
  - Nhận diện nhu cầu qua ngôn ngữ tự nhiên tiếng Việt
- **Quản lý đơn hàng:** Theo dõi trạng thái, lịch sử mua sắm, hủy đơn
- **Đánh giá & Bình luận:** Review sản phẩm 5 sao (dành cho đã nhận hàng)

### 🛠 Dành Cho Quản Trị Viên
- **Dashboard thống kê:** Biểu đồ doanh thu, đơn hàng theo trạng thái (Chart.js)
- **Quản lý sản phẩm:** CRUD cây cảnh, cập nhật tồn kho, upload ảnh
- **Quản lý đơn hàng:** Duyệt đơn, cập nhật trạng thái vận chuyển
- **Quản lý Chatbot:** Cấu hình từ khóa và kịch bản AI

---

## 🤖 Hệ Thống AI Chatbot

Chatbot sử dụng **Google Gemini API** kết hợp **RAG (Retrieval-Augmented Generation)**:

```text
Câu hỏi người dùng → Nhận diện ý định (Gemini) 
→ Truy xuất dữ liệu cây cảnh từ Database (RAG) 
→ Tổng hợp thông tin & Trả lời tự nhiên (Gemini)
```

**Các tính năng thông minh:**
- Gợi ý cây cảnh dựa trên điều kiện ánh sáng, giá cả, và kinh nghiệm chăm sóc.
- Trả lời chi tiết về đặc tính và cách chăm sóc của từng loại cây.
- So sánh sự khác nhau giữa các loại cây để giúp khách hàng dễ lựa chọn.
- Duy trì ngữ cảnh hội thoại qua nhiều lượt chat bằng Django Sessions.

---

## 📂 Cấu Trúc Dự Án

```
plant_shop_website/
├── manage.py                   # Django management script
├── requirements.txt            # Danh sách thư viện
├── README.md                   # Tài liệu dự án (file này)
├── work_assignment.md          # Phân công công việc nhóm
├── db.sqlite3                  # Database SQLite
│
├── plant_shop/                 # Project Settings (settings.py, urls.py)
├── products/                   # App: Quản lý Sản phẩm & Danh mục
├── orders/                     # App: Giỏ hàng & Đơn hàng
├── users/                      # App: Tài khoản & Hồ sơ
├── reviews/                    # App: Đánh giá & Bình luận
├── plant_recommendation/       # App: AI Chatbot (Gemini API + RAG)
│   ├── ai_service.py           # Logic tích hợp Gemini và RAG
│   ├── generate_data.py        # Tạo dữ liệu vector
│   ├── chatbot_config.json     # Prompt và config cho chatbot
│   └── selected_plants.json    # Dữ liệu cache về cây cảnh
│
├── templates/                  # HTML Templates (Bootstrap 5)
├── static/                     # CSS, JS, Images
├── media/                      # File upload (Ảnh sản phẩm, Avatar)
└── scripts/                    # Utility scripts (Seed data, Import)
```

---

## 📦 Cài Đặt & Chạy Dự Án

### 1. Clone Dự Án
```bash
git clone https://github.com/tuanlamviec007/plant_shop_website.git
cd plant_shop_website
```

### 2. Tạo Môi Trường Ảo
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Cài Đặt Thư Viện
```bash
pip install -r requirements.txt
```

### 4. Khởi Tạo Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo Tài Khoản Admin
```bash
python manage.py createsuperuser
```

### 6. (Tùy Chọn) Import Dữ Liệu Mẫu
```bash
python scripts/import_dataset.py
python scripts/add_missing_plants.py
```

### 7. Chạy Server
```bash
python manage.py runserver
```
Truy cập: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Tài Khoản Mẫu

| Vai Trò | Username | Password |
|---------|----------|----------|
| **Admin** | admin | *(tự tạo bằng createsuperuser)* |
| **User thường** | *(tự đăng ký tại /register/)* | *(tự đặt)* |

**Trang Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🏗 Công Nghệ Sử Dụng

| Hạng Mục | Công Nghệ |
|----------|-----------|
| **Backend** | Django 5.0, Python 3.13 |
| **Database** | SQLite 3 + Django ORM |
| **Frontend** | Bootstrap 5.3, HTML5, CSS3, JavaScript |
| **AI/NLP** | Google Gemini API (RAG Architecture) |
| **Biểu Đồ** | Chart.js |
| **Version Control** | Git / GitHub |

---

## 👥 Nhóm 5

| Thành Viên | Vai Trò | Nhiệm Vụ |
|------------|---------|---------|
| **Nguyễn Đắc Tuấn** | Frontend + AI | Templates HTML, Chatbot NLP, AI Training |
| **Đàm Trường Vũ** | Backend | Models, Views, Admin, Database |
| **Nguyễn Thị Mai Anh** | Báo Cáo + QA | Báo cáo Word, Slide, Testing, Seed Data |

---

## 📄 Tài Liệu Dự Án

- 📋 **Phân công:** (Đã hoàn thành)
- 🔧 **SRS:** Xem trong tài liệu báo cáo đính kèm
- 📊 **ERD & Use Case:** Xem trong tài liệu báo cáo đính kèm
- 🤖 **Kiến trúc AI:** Xem trong tài liệu báo cáo đính kèm

---

*🌱 Dự án phục vụ mục đích học tập – Nhóm 5, 2026.*