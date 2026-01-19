# HƯỚNG DẪN SỬ DỤNG PLANT SHOP

Chào mừng bạn đến với Plant Shop - Cửa hàng cây cảnh mini uy tín. Tài liệu này sẽ hướng dẫn chi tiết cách sử dụng các tính năng trên website cho cả Người dùng và Quản trị viên.

---

## I. HƯỚNG DẪN CHO NGƯỜI DÙNG (USER)

### 1. Đăng ký và Đăng nhập
- **Đăng ký**: 
  - Truy cập vào link "Đăng ký" trên thanh menu.
  - Điền đầy đủ thông tin: Tên đăng nhập, Email, Mật khẩu.
  - Sau khi đăng ký thành công, bạn có thể đăng nhập ngay.
- **Đăng nhập**: 
  - Sử dụng Tên đăng nhập và Mật khẩu đã đăng ký để truy cập vào hệ thống.
  - Đăng nhập giúp bạn lưu giỏ hàng và xem lịch sử đơn hàng.

### 2. Tìm kiếm và Mua hàng
- **Duyệt sản phẩm**: 
  - Truy cập trang "Sản phẩm" để xem toàn bộ cây cảnh.
  - Sử dụng bộ lọc bên trái để tìm theo: Danh mục, Độ khó chăm sóc, Khoảng giá.
  - Sử dụng thanh tìm kiếm để tìm theo tên cây.
- **Giỏ hàng & Thanh toán**:
  - Nhấn nút "Thêm vào giỏ" ở trang danh sách hoặc chi tiết sản phẩm.
  - Vào "Giỏ hàng" để xem lại các sản phẩm đã chọn, cập nhật số lượng hoặc xóa bớt.
  - Nhấn "Thanh toán" và điền thông tin giao hàng để hoàn tất đặt hàng.

### 3. Tính năng Nhận diện Cây bằng AI (Mới & Chính xác cao)
Đây là tính năng đặc biệt giúp bạn nhận diện tên cây thông qua hình ảnh với độ chính xác rất cao.

**Cách sử dụng:**
1.  **Truy cập**: Nhấn vào menu "Nhận diện AI" trên thanh điều hướng.
2.  **Tải ảnh lên**: 
    - Nhấn vào khu vực upload hoặc nút chọn ảnh.
    - Chọn một bức ảnh rõ nét về cây bạn muốn nhận diện.
3.  **Nhận kết quả**:
    - Hệ thống AI sẽ phân tích hình ảnh trong vài giây.
    - Kết quả trả về bao gồm: Tên cây, Độ chính xác (%), và gợi ý sản phẩm tương ứng tại cửa hàng.
    - Bạn có thể nhấn vào sản phẩm gợi ý để xem chi tiết và đặt mua ngay.
4.  **Lịch sử**: Bạn có thể xem lại các lần nhận diện trước đó trong tab "Lịch sử".

> **Lưu ý**: Để có kết quả chính xác nhất, hãy chụp ảnh cây ở điều kiện đủ sáng và trọn vẹn chủ thể.

### 4. Quản lý Tài khoản
- Vào menu "Hồ sơ" để cập nhật thông tin cá nhân.
- Xem lại "Đơn hàng" để theo dõi trạng thái các đơn hàng đã đặt.

---

## II. HƯỚNG DẪN CHO QUẢN TRỊ VIÊN (ADMIN)

### 1. Truy cập Trang Quản trị
- Truy cập đường dẫn: `/admin/` (Ví dụ: `http://ten-mien-website.com/admin/`).
- Đăng nhập bằng tài khoản có quyền Superuser hoặc Staff.

### 2. Quản lý Sản phẩm
- Tại mục **Products**, chọn **Products**.
- **Thêm mới**: Nhấn nút "Add product" ở góc phải. Điền tên, giá, mô tả, tải ảnh và chọn danh mục.
- **Chỉnh sửa**: Nhấn vào tên sản phẩm để sửa thông tin.
- **Xóa**: Chọn sản phẩm và chọn hành động "Delete" hoặc nút xóa ở trang chi tiết.

### 3. Quản lý Đơn hàng
- Tại mục **Orders**, chọn **Orders**.
- Bạn có thể xem danh sách tất cả đơn hàng.
- Nhấn vào mã đơn hàng để xem chi tiết: Sản phẩm, Người mua, Địa chỉ.
- Cập nhật trạng thái đơn hàng (Ví dụ: Chuyển từ "Pending" sang "Shipped") và lưu lại.

### 4. Quản lý Người dùng
- Tại mục **Authentication and Authorization**, chọn **Users**.
- Bạn có thể thêm người dùng mới, reset mật khẩu, hoặc phân quyền (cho phép truy cập admin).

### 5. Quản lý Dữ liệu AI
- Tại mục **Ai_Recognition**, bạn có thể xem **Plant recognitions**.
- Đây là nơi lưu trữ logs lịch sử nhận diện của người dùng, giúp bạn thống kê nhu cầu tìm kiếm của khách hàng.

---

*Cảm ơn bạn đã sử dụng Plant Shop! Mọi thắc mắc xin liên hệ bộ phận hỗ trợ.*
