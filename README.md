# Supermarket-Electronics-Management
Enterprise-Level Mini Project for Programming Methods Course

**Instructor:** Ts. Trần Văn Long  
**Author:** Đỗ Hải Âu

---

# I. GIỚI THIỆU HỆ THỐNG
Dự án **Hệ thống Quản lý Siêu thị Điện máy Đa phân tầng** là một ứng dụng phần mềm mini-project hoàn chỉnh được nghiên cứu và xây dựng trong khuôn khổ học phần **Phương pháp lập trình** (Programming Methods) do Thầy Long trực tiếp giảng dạy. 

Khác với các phương pháp lập trình thủ tục (Procedural) thông thường dễ dẫn đến mã nguồn bị rối (Spaghetti Code), dự án này được định hướng thiết kế ngay từ đầu theo phương pháp **Lập trình hướng đối tượng (OOP) chuyên sâu** kết hợp với kiến trúc phân tầng chuẩn doanh nghiệp (**Layered Architecture - 3 Layers**). Mục tiêu cốt lõi của hệ thống là giải quyết bài toán quản lý kho hàng điện máy phức tạp, tự động hóa quy trình tính toán giá bán đặc thù dựa trên cấu trúc đa hình, xử lý đồng bộ chuỗi giao dịch mua hàng (Transaction) và quản lý cơ sở dữ liệu quan hệ thông qua **SQLite DBMS**.

---

# II. CÁC TÍNH NĂNG NỔI BẬT & CƠ CHẾ VẬN HÀNH

## 1. Quản lý cơ bản (CRUD Nghiệp vụ Kho)
* **Thêm sản phẩm (Create):** Hệ thống không quản lý hàng hóa chung chung mà phân tách thành các thực thể vật lý cụ thể bao gồm `Laptop` (quản lý RAM, CPU), `Phone` (quản lý Pin, Camera) và `Fridge` (quản lý Dung tích tủ). Quá trình thêm mới kiểm tra chặt chẽ tính duy nhất của Mã sản phẩm (`product_id`) nhằm tránh xung đột dữ liệu.
* **Hiển thị danh sách (Read):** Dữ liệu được truy vấn từ bảng cơ sở dữ liệu và chuyển đổi ngược thành một danh sách các Object. Tầng hiển thị sử dụng định dạng bảng CLI căn lề tự động, đồng thời nhúng các mã màu ANSI để tạo hiệu ứng thị giác trực quan. Đặc biệt, hệ thống tích hợp cơ chế **Cảnh báo tồn kho động (Dynamic Stock Alert)**: Tự động nhuộm đỏ và hiển thị `(Hết)` nếu tồn kho bằng 0, hoặc nhuộm vàng kèm chữ `(Ít)` nếu số lượng tồn kho đạt mức cảnh báo (`<= 3`).
* **Cập nhật tồn kho (Update):** Cho phép thủ kho điều chỉnh chính xác số lượng hàng hóa nhập kho bổ sung hoặc kiểm kê định kỳ dựa trên mã ID sản phẩm.
* **Xóa sản phẩm (Delete):** Cho phép gỡ bỏ một mã hàng hóa không còn kinh doanh ra khỏi hệ thống. Thao tác yêu cầu xác nhận `(y/n)` để tránh bấm nhầm và sử dụng cơ chế xóa vật lý thông qua câu lệnh SQL an toàn.

## 2. Xử lý Logic nâng cao (Advanced Logic)
* **Tìm kiếm chuỗi con gần đúng (Substring Search):** Hệ thống tích hợp tính năng tìm kiếm thông minh. Khi người dùng nhập một từ khóa (Ví dụ: "Mac" hoặc "Samsung"), hệ thống sẽ sử dụng mệnh đề `LIKE %keyword%` của SQL tại tầng Service để quét toàn bộ bảng dữ liệu. Bất kỳ sản phẩm nào chứa chuỗi ký tự đó trong tên đều được trích xuất và hiển thị.
* **Logic Giao dịch phức tạp (Transaction & Rollback):** Đây là tính năng nâng cao cốt lõi nhằm đảm bảo tính toàn vẹn dữ liệu theo nguyên lý **ACID**. Khi khách hàng tạo một đơn hàng chứa nhiều sản phẩm (Giỏ hàng):
    1. *Giai đoạn Kiểm tra (Validation Phase):* Hệ thống duyệt qua tất cả sản phẩm trong giỏ để kiểm tra số lượng tồn kho hiện tại có đủ đáp ứng hay không.
    2. *Giai đoạn Thực thi (Execution Phase):* Nếu tất cả đều đủ hàng, hệ thống tiến hành ghi dữ liệu vào bảng `invoices`, ghi nhiều dòng vào bảng `invoice_items` và trừ kho đồng loạt các sản phẩm tương ứng.
    3. *Giai đoạn Bảo vệ (Rollback Phase):* Nếu có bất kỳ lỗi nào xảy ra giữa chừng (ví dụ: món hàng thứ 3 bị hết kho trong lúc đang chạy dở), hệ thống sẽ kích hoạt lệnh `rollback` để khôi phục kho của món hàng thứ 1 và thứ 2 về nguyên trạng, ngăn chặn tuyệt đối tình trạng sai lệch kho.
* **Thống kê gom nhóm nâng cao (Grouped Statistics):** Hệ thống tự động thực hiện các câu lệnh truy vấn phức tạp kết hợp hàm tổng hợp (`SUM`, `COUNT`) và mệnh đề `GROUP BY product_id` để phân tích lịch sử bán hàng. Từ đó, chương trình tự động tính toán chính xác tổng doanh thu, tổng số đơn và tìm ra **Top 3 sản phẩm bán chạy nhất** dựa trên tổng sản lượng đã xuất kho.

## 3. Sắp xếp & Định dạng Dữ liệu Bền vững
* **Sắp xếp đa hình (Polymorphic Sorting):** Tính năng sắp xếp các sản phẩm theo giá bán giảm dần không sử dụng các câu lệnh rẽ nhánh `if-else` thủ công để kiểm tra loại sản phẩm. Thay vào đó, thuật toán tận dụng triệt để tính **Đa hình động**. Khi hàm sắp xếp duyệt qua danh sách, mỗi đối tượng `Laptop`, `Phone`, hay `Fridge` sẽ tự động gọi phương thức `calculate_final_price()` của riêng mình (Laptop cộng 10% thuế linh kiện, Phone cộng 5% phí môi trường, Fridge cộng phí cồng kềnh) để làm tiêu chí xếp hạng.
* **Cơ sở dữ liệu SQLite:** Toàn bộ vòng đời dữ liệu được lưu trữ trong tệp tin quan hệ `store.db`. Dữ liệu không bị mất đi khi tắt chương trình, loại bỏ hoàn toàn nhược điểm ghi đè thủ công của file TXT hay JSON thông thường.
* **Xuất tệp cấu trúc CSV:** Hệ thống hỗ trợ tính năng kết xuất dữ liệu báo cáo kinh doanh ra file `sales_report.csv`. Mã nguồn sử dụng thư viện `csv` kết hợp cấu hình mã hóa mã `utf-8-sig` giúp Thầy giáo khi mở file trực tiếp bằng Microsoft Excel sẽ thấy font chữ Tiếng Việt hiển thị đẹp đẽ, hoàn hảo mà không bị lỗi ký tự.

---

# III. KIẾN TRÚC PHÂN TẦNG CỦA MÃ NGUỒN (LAYERED ARCHITECTURE)

Dự án được phân tách nghiêm ngặt thành **3 tầng độc lập (3-Tier Layered Architecture)** nhằm đảm bảo tính dễ bảo trì, dễ mở rộng và cô lập lỗi:

       ┌────────────────────────────────────────────────────────┐
       │                 TẦNG GIAO DIỆN (VIEWS)                 │
       │     - views/menu_view.py (Chỉ in bảng & nhận phím)      │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Gọi Service)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                TẦNG NGHIỆP VỤ (SERVICES)               │
       │     - store_service.py (Thuật toán, Sắp xếp đa hình)   │
       │     - invoice_service.py (Transaction, Thống kê DB)    │
       └───────────────────────────┬────────────────────────────┘
                                   │ (Query SQL / Đọc ghi)
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │               TẦNG DỮ LIỆU & MÔ HÌNH (MODELS)          │
       │     - models/product.py (OOP Encapsulation/Inherit)    │
       │     - services/database.py (Khởi tạo kết nối SQLite)   │
       └────────────────────────────────────────────────────────┘

#IV. Bảng tự chấm điểm:

# Supermarket-Electronics-Management
Enterprise-Level Mini Project for Programming Methods Course

## I. GIỚI THIỆU HỆ THỐNG
Dự án Hệ thống Quản lý Siêu thị Điện máy Đa phân tầng được xây dựng theo mô hình Lập trình hướng đối tượng (OOP) chuyên sâu kết hợp với kiến trúc phân tầng chuẩn doanh nghiệp (Layered Architecture - 3 Layers) bằng ngôn ngữ Python.

## II. BẢNG TỰ CHẤM ĐIỂM (CRITERIA EVALUATION MATRIX)

| Thành phần | Tiêu chí chi tiết chấm điểm | Giải thích cơ chế & Cách thức thực hiện trong dự án | Trạng thái | Điểm |
| :--- | :--- | :--- | :---: | :---: |
| **1. CLI Menu** | Menu dùng vòng lặp vô hạn, xử lý lỗi nhập liệu, có màu sắc ANSI. | Triển khai tại hàm `MenuView.run()` dùng vòng lặp `while True` phối hợp mã màu ANSI. | ✅ Đạt | **1.0** |
| **2. Input Validation** | Thêm bản ghi mới, kiểm tra và ràng buộc dữ liệu đầu vào. | Khối `try-except ValueError` trong `add_product_menu` và Setter trong lớp `Product` chặn dữ liệu âm. | ✅ Đạt | **1.0** |
| **3. Data Display** | In danh sách bản ghi rõ ràng, căn lề chuẩn theo dạng bảng. | Hàm `view_products` sử dụng `f-string` định dạng độ rộng cột cố định (`{p.name:<22}`) giúp bảng thẳng hàng. | ✅ Đạt | **1.0** |
| **4. Basic Search** | Tìm kiếm bản ghi theo ID hoặc theo tên gần đúng. | Hàm `search_by_name` sử dụng truy vấn SQL: `SELECT * FROM products WHERE name LIKE ?`. | ✅ Đạt | **1.0** |
| **5. Sorting** | Sắp xếp danh sách theo trường dữ liệu (Giá giảm dần). | Hàm `sort_by_price_desc` tận dụng tính Đa hình động gọi `p.calculate_final_price()` của từng đối tượng con. | ✅ Đạt | **1.0** |
| **6. Calculation** | Tính toán thống kê dữ liệu cơ bản (Tính tổng, tính đếm). | Hàm `get_revenue_report` thực hiện SQL: `SELECT SUM(final_total), COUNT(*) FROM invoices`. | ✅ Đạt | **1.0** |
| **7. Architecture** | Áp dụng cấu trúc phân tầng (3 Layers), mã nguồn sạch. | Dự án chia tách độc lập thành 3 thư mục tầng rõ rệt: `models/`, `services/`, `views/`. Tuân thủ PEP 8. | ✅ Đạt | **1.0** |
| **8. Complex Logic** | Xử lý logic nghiệp vụ nâng cao (Transaction & Rollback). | Hàm `create_invoice` gọi lệnh `conn.commit()` khi thành công và gọi `conn.rollback()` để hoàn kho nếu lỗi. | ✅ Đạt | **1.0** |
| **9. DBMS Storage** | Lưu trữ dữ liệu bền vững sử dụng Hệ quản trị CSDL. | Tích hợp hệ quản trị cơ sở dữ liệu quan hệ **SQLite** (`store.db`) với ràng buộc khóa ngoại (`FOREIGN KEY`). | ✅ Đạt | **1.0** |
| **10. Git & OOP** | Sử dụng Git/GitHub, OOP đầy đủ, xuất báo cáo CSV. | Áp dụng Đóng gói, Kế thừa, Trừu tượng; hàm `export_sales_report_csv()` xuất báo cáo ra file CSV hiển thị tiếng Việt. | ✅ Đạt | **1.0** |
| **TỔNG CỘNG** | *(Dự án đáp ứng xuất sắc toàn bộ barem điểm)* | | | **10.0** |
