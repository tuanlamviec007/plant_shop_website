# PHÂN TÍCH HOẠT ĐỘNG HỆ THỐNG VÀ QUYỀN QUẢN TRỊ (ADMIN)

Tài liệu này mô tả chi tiết quy trình hoạt động của hệ thống Plant Shop và các công cụ quản lý dành cho Admin.

---

## 1. Quy Trình Hoạt Động (User Flow)

### 1.1 Khách hàng (User Journey)
Quá trình mua sắm của khách hàng diễn ra theo luồng sau:
1.  **Tìm kiếm & Xem sản phẩm:**
    - Khách hàng duyệt danh sách cây theo danh mục (Sen đá, Xương rồng...) hoặc tìm kiếm theo tên.
    - Hệ thống hỗ trợ lọc theo mức độ chăm sóc (Dễ, Trung bình, Khó) và ánh sáng.
2.  **AI Tư vấn (Điểm nổi bật):**
    - Nếu khách chưa biết mua cây gì hoặc có ảnh cây lạ, họ dùng tính năng **Nhận diện AI**.
    - Hệ thống trả về tên cây, độ chính xác và gợi ý sản phẩm tương ứng trong cửa hàng.
3.  **Mua hàng:**
    - Khách thêm cây vào Giỏ hàng.
    - Tại trang Checkout, khách nhập thông tin giao hàng.
    - Đơn hàng được tạo với trạng thái `Pending` (Chờ xử lý).
4.  **Sau mua hàng:**
    - Khách nhận email xác nhận (giả lập).
    - Khách có thể xem lịch sử đơn hàng và theo dõi trạng thái.
    - Sau khi nhận hàng, khách có thể đánh giá và bình luận sản phẩm.

### 1.2 Hệ thống xử lý (System Logic)
- **Tồn kho (Auto Stock Management):**
    - Khi Admin xác nhận đơn (`Pending` -> `Confirmed`), hệ thống **tự động trừ** số lượng tồn kho.
    - Nếu đơn bị hủy (`Confirmed` -> `Cancelled`), hệ thống **tự động hoàn** lại số lượng vào kho.
- **Bảo mật:**
    - Password được mã hóa (PBKDF2).
    - Session quản lý giỏ hàng cho cả khách vãng lai.

---

## 2. Phân Tích Quyền Admin & Chức Năng Quản Trị

Admin truy cập qua đường dẫn `/admin/`. Giao diện được tùy biến để quản lý hiệu quả các nghiệp vụ sau:

### 2.1 Quản lý Sản phẩm & Danh mục (`Products` App)
**Chức năng:**
- **Danh sách tổng quan:** Xem tên, giá, tồn kho, số lượng đã bán, đánh giá trung bình.
- **Lọc & Tìm kiếm:** Lọc theo danh mục, trạng thái (ẩn/hiện), sản phẩm nổi bật. Tìm kiếm theo tên.
- **Chỉnh sửa nhanh:** Có thể sửa giá và tồn kho trực tiếp từ danh sách mà không cần vào chi tiết.
- **Cấu hình hiển thị:** Đặt sản phẩm là "Nổi bật" để hiện lên trang chủ.

### 2.2 Quản lý Đơn hàng (`Orders` App) - QUAN TRỌNG
Đây là nới xử lý nghiệp vụ bán hàng chính.
- **Xem chi tiết:** Mã đơn, khách hàng, tổng tiền, phương thức thanh toán.
- **Xử lý đơn hàng (Workflow):**
    - Admin thay đổi trạng thái đơn: `Pending` -> `Confirmed` -> `Shipping` -> `Delivered`.
    - **Tự động hóa:** Khi Admin chuyển sang `Confirmed`, code sẽ tự động trừ kho. Admin không cần trừ tay.
- **Chi tiết sản phẩm trong đơn:** Xem danh sách các cây khách mua trong cùng 1 đơn (Inline view).

### 2.3 Quản lý Đánh giá (`Reviews` App)
- **Kiểm duyệt:** Admin có quyền duyệt (`is_approved`) các bình luận trước khi cho hiển thị lên web.
- **Theo dõi:** Xem ai đánh giá, rating bao nhiêu sao.

### 2.4 Quản lý AI (`AI Recognition` App)
- **Monitoring:** Admin xem được lịch sử các lần nhận diện của khách hàng.
- **Dữ liệu:** Xem ảnh khách upload, kết quả AI trả về và độ tin cậy (confidence score) để cải thiện model sau này.

### 2.5 Quản lý Người dùng (`Users` App)
- **Hồ sơ:** Xem thông tin chi tiết (Phone, Address) đi kèm với tài khoản User.
- **Phân quyền:** Có thể cấp quyền Staff/Admin cho user khác hoặc khóa tài khoản vi phạm.

---

## 3. Bảng Tổng Hợp Quyền

| Vai trò | Xem Sản phẩm | Mua hàng | Upload Ảnh AI | Quản lý Kho | Duyệt Đơn | Xóa User |
|:-------:|:------------:|:--------:|:-------------:|:-----------:|:---------:|:--------:|
| Guest   | ✅           | ❌ (*)   | ❌            | ❌          | ❌        | ❌       |
| User    | ✅           | ✅       | ✅            | ❌          | ❌        | ❌       |
| Admin   | ✅           | ✅       | ✅            | ✅          | ✅        | ✅       |

*(*) Guest có thể thêm vào giỏ nhưng cần đăng nhập để thanh toán.*

## 4. Đặc điểm Kỹ thuật Nổi bật trong Code
1.  **Signal/Model Override:** Logic trừ tồn kho được viết trong phương thức `save_model` của `OrderAdmin` hoặc `save` của Model, đảm bảo tính nhất quán dữ liệu.
2.  **Inline Admin:** Sử dụng `OrderItemInline` để hiển thị sản phẩm ngay trong trang chi tiết đơn hàng, giúp Admin thao tác nhanh.
3.  **Slugify:** Tự động tạo URL thân thiện (slug) từ tên sản phẩm tiếng Việt.
