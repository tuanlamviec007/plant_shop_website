# Phân Công Công Việc Chi Tiết - Dự Án Plant Shop Website

## Tổng Quan Dự Án
Website bán cây cảnh với chatbot AI tư vấn, sử dụng Django framework. Bao gồm các module: `products`, `orders`, `users`, `reviews`, `plant_recommendation` (AI chatbot).

**Lưu ý:** Dự án chạy trên môi trường local, được thực hiện bởi sinh viên. Báo cáo cuối cùng bao gồm bản Word và slide thuyết trình do Mai Anh chịu trách nhiệm chính.

---

## Phân Công Theo Thành Viên

### 👨‍💻 1. Nguyễn Đắc Tuấn - Frontend + Chatbot AI + Hỗ Trợ Báo Cáo
**Vai Trò Chính:** Phát triển giao diện người dùng và hệ thống chatbot AI.

#### A. Frontend Development
| Nhiệm Vụ | File/Thư Mục | Trạng Thái |
|---|---|---|
| Thiết kế layout chung | `templates/base.html` | ✅ Hoàn thành |
| Trang chủ | `templates/home.html` | ✅ Hoàn thành |
| Header, Footer, Navigation | `templates/includes/` | ✅ Hoàn thành |
| Danh sách & Chi tiết sản phẩm | `templates/products/` | ✅ Hoàn thành |
| Giỏ hàng, Thanh toán, Lịch sử đơn hàng | `templates/orders/` | ✅ Hoàn thành |
| Đăng nhập, Đăng ký, Profile | `templates/users/` | ✅ Hoàn thành |
| Đánh giá sản phẩm | `templates/reviews/` | ✅ Hoàn thành |
| CSS Styling | `static/css/` | ✅ Hoàn thành |
| JavaScript Interactions | `static/js/` | ✅ Hoàn thành |
| Tích hợp Bootstrap 5, Responsive | Toàn bộ templates | ✅ Hoàn thành |

#### B. Chatbot AI Development
| Nhiệm Vụ | File | Trạng Thái |
|---|---|---|
| Xử lý NLP, Intent Classification | `plant_recommendation/ai_service.py` | ✅ Hoàn thành |
| API endpoints cho chat | `plant_recommendation/views.py` | ✅ Hoàn thành |
| Cấu hình chatbot | `plant_recommendation/chatbot_config.json` | ✅ Hoàn thành |
| Dữ liệu cây trồng curated | `plant_recommendation/selected_plants.json` | ✅ Hoàn thành |
| Tối ưu hóa hiệu suất chatbot | `ai_service.py` (optimize) | ✅ Hoàn thành |

#### C. Hỗ Trợ AI Training (Cùng Mai Anh)
| Nhiệm Vụ | File | Trạng Thái |
|---|---|---|
| Thu thập & chuẩn bị training data | `plant_recommendation/training_data.json` | ✅ Hoàn thành |
| Dataset intent classification | `plant_recommendation/generate_data.py` | ✅ Hoàn thành |
| Chạy script training model | `plant_recommendation/train_model.py` | ✅ Hoàn thành |
| Model đã huấn luyện | `plant_recommendation/intent_model.pkl` | ✅ Hoàn thành |

#### D. Hỗ Trợ Báo Cáo
- Phát triển giao diện Dashboard Admin (biểu đồ, thống kê)
- Tạo templates hiển thị dữ liệu báo cáo
- Nhận hỗ trợ logic backend báo cáo từ Vũ (thống kê, xuất dữ liệu)

**Thời Gian Dự Kiến:** 4–5 tuần | **Công Cụ:** HTML, CSS, JS, Bootstrap, Django Templates, scikit-learn, underthesea

---

### 👨‍💻 2. Đàm Trường Vũ - Backend + Database + Deployment & Optimization
**Vai Trò Chính:** Phát triển backend logic, thiết kế CSDL, đảm bảo hệ thống vận hành ổn định.

#### A. Backend Development (Models & Views)
| Nhiệm Vụ | File | Trạng Thái |
|---|---|---|
| Model Product, Category | `products/models.py` | ✅ Hoàn thành |
| Model Order, OrderItem, Cart | `orders/models.py` | ✅ Hoàn thành |
| Model UserProfile (Auth) | `users/models.py` | ✅ Hoàn thành |
| Model Review, Rating | `reviews/models.py` | ✅ Hoàn thành |
| Model ChatSession, ChatMessage | `plant_recommendation/models.py` | ✅ Hoàn thành |
| CRUD sản phẩm, tìm kiếm, lọc | `products/views.py` | ✅ Hoàn thành |
| Xử lý đơn hàng, thanh toán | `orders/views.py` | ✅ Hoàn thành |
| Authentication, Profile | `users/views.py` | ✅ Hoàn thành |
| Quản lý đánh giá | `reviews/views.py` | ✅ Hoàn thành |
| Admin interface | `*/admin.py` | ✅ Hoàn thành |
| Database migrations | `*/migrations/` | ✅ Hoàn thành |

#### B. Deployment & Optimization
| Nhiệm Vụ | Trạng Thái |
|---|---|
| Thiết lập virtual environment | ✅ Hoàn thành |
| Tối ưu hóa database queries (index) | ✅ Hoàn thành |
| Bảo mật: hash password, CSRF, validation | ✅ Hoàn thành |
| Viết unit tests backend | 🔄 Đang thực hiện |
| Seed data & import dataset | ✅ Hoàn thành |
| Chuẩn bị `requirements.txt` | ✅ Hoàn thành |

#### C. Hỗ Trợ Logic Báo Cáo (Cùng Mai Anh)
- Cung cấp logic thống kê doanh thu, số đơn hàng cho Dashboard
- Hỗ trợ xuất dữ liệu báo cáo

**Thời Gian Dự Kiến:** 5–6 tuần | **Công Cụ:** Django, Python, SQLite, Django Admin

---

### 👩‍💼 3. Nguyễn Thị Mai Anh - Báo Cáo + Hỗ Trợ AI Training + Test & Dữ Liệu
**Vai Trò Chính:** Chịu trách nhiệm chính về **báo cáo cuối cùng** (Word + Slide), hỗ trợ AI training và đảm bảo chất lượng dữ liệu/kiểm thử.

#### A. Báo Cáo Cuối Cùng (Nhiệm Vụ Chính)
| Nhiệm Vụ | Sản Phẩm | Trạng Thái |
|---|---|---|
| Viết báo cáo Word 25–30 trang | `BaoCao_PlantShop.docx` | 🔄 Đang thực hiện |
| Thiết kế Slide thuyết trình 10–15 trang | `Slide_PlantShop.pptx` | 🔄 Đang thực hiện |
| Mục tiêu & phạm vi dự án | Chương 1 báo cáo | 🔄 Đang thực hiện |
| Phân tích yêu cầu (SRS) | Chương 2 báo cáo | 🔄 Đang thực hiện |
| Thiết kế hệ thống (ERD, Use Case) | Chương 3 báo cáo | 🔄 Đang thực hiện |
| Triển khai & phát triển | Chương 4 báo cáo | 🔄 Đang thực hiện |
| Kết quả testing | Chương 5 báo cáo | 🔄 Đang thực hiện |
| Kết luận & hướng phát triển | Chương 6 báo cáo | 🗓️ Kế hoạch |

#### B. Dashboard & Báo Cáo Hệ Thống
- Phát triển views và templates cho Admin Dashboard
- Tích hợp biểu đồ Chart.js (doanh thu, đơn hàng, sản phẩm bán chạy)
- Hỗ trợ xuất báo cáo dạng PDF/Excel

#### C. Hỗ Trợ Training AI (Cùng Tuấn)
| Nhiệm Vụ | File | Trạng Thái |
|---|---|---|
| Thu thập dữ liệu training | `training_data.json` | ✅ Hoàn thành |
| Validate dataset | `generate_data.py` | ✅ Hoàn thành |
| Chạy & đánh giá model | `train_model.py` | ✅ Hoàn thành |

#### D. Test & Cập Nhật Dữ Liệu
| Nhiệm Vụ | Trạng Thái |
|---|---|
| Test đăng nhập/đăng ký | ✅ Hoàn thành |
| Test giỏ hàng & đặt hàng | ✅ Hoàn thành |
| Test chatbot AI | ✅ Hoàn thành |
| Test tìm kiếm, lọc sản phẩm | ✅ Hoàn thành |
| Test responsive design | ✅ Hoàn thành |
| Import dữ liệu từ CSV | `scripts/import_dataset.py` | ✅ Hoàn thành |
| Thêm dữ liệu cây mới | `scripts/add_missing_plants.py` | ✅ Hoàn thành |
| Cập nhật `requirements.txt` | ✅ Hoàn thành |

**Thời Gian Dự Kiến:** 4–5 tuần | **Công Cụ:** Microsoft Word, PowerPoint, Python, Django Testing, Chart.js

---

## Lịch Trình Chung

| Tuần | Nhiệm Vụ Chính | Người Phụ Trách |
|---|---|---|
| Tuần 1–2 | Setup project, phân tích yêu cầu, thiết kế database | Vũ (chính), Tuấn, Mai Anh |
| Tuần 3–4 | Phát triển core features (products, orders, users) | Vũ (backend), Tuấn (frontend) |
| Tuần 5–6 | Chatbot AI, Báo cáo Dashboard, Training AI | Tuấn & Mai Anh (chính) |
| Tuần 7–8 | Testing, optimization, báo cáo, slide | Mai Anh (chính), Vũ (support) |

---

## Quy Tắc Phối Hợp
- **Tuấn & Vũ:** Phối hợp chặt chẽ trong tích hợp frontend ↔ backend
- **Tuấn & Mai Anh:** Phối hợp trong AI training và chatbot testing
- **Vũ & Mai Anh:** Phối hợp trong backend logic báo cáo và testing
- **Code Review:** Review code trước khi merge vào nhánh chính
- **Commit chuẩn:** Commit message rõ ràng, ít nhất 20 commit tổng nhóm

---

## Công Cụ Và Công Nghệ

| Hạng Mục | Công Nghệ |
|---|---|
| Framework | Django 5.0 |
| Database | SQLite (dev), PostgreSQL (prod option) |
| Frontend | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5 |
| AI/NLP | Python, scikit-learn, underthesea |
| Biểu đồ | Chart.js |
| Testing | Django Test Framework |
| Version Control | Git / GitHub |
| Tài liệu | Microsoft Word, PowerPoint |

---

## Tiêu Chí Đánh Giá Nội Bộ
- **Chức Năng:** Hoạt động đúng yêu cầu, không lỗi nghiêm trọng
- **Hiệu Suất:** Response time < 2s, chatbot accuracy > 80%
- **UI/UX:** Responsive, thân thiện người dùng
- **Code Quality:** Clean code, có comment, đúng MVC
- **Bảo Mật:** Hash password, CSRF protection, input validation
- **Tài Liệu:** Báo cáo Word 25–30 trang, Slide 10–15 trang rõ ràng chuyên nghiệp