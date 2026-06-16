# Supermarket-Electronics-Management
Enterprise-Level Mini Project for Programming Methods Course
**Instructor:** Ts. Trần Văn Long 
**Author:**Đỗ Hải Âu

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
    1.  *Giai đoạn Kiểm tra (Validation Phase):* Hệ thống duyệt qua tất cả sản phẩm trong giỏ để kiểm tra số lượng tồn kho hiện tại có đủ đáp ứng hay không.
    2.  *Giai đoạn Thực thi (Execution Phase):* Nếu tất cả đều đủ hàng, hệ thống tiến hành ghi dữ liệu vào bảng `invoices`, ghi nhiều dòng vào bảng `invoice_items` và trừ kho đồng loạt các sản phẩm tương ứng.
    3.  *Giai đoạn Bảo vệ (Rollback Phase):* Nếu có bất kỳ lỗi nào xảy ra giữa chừng (ví dụ: món hàng thứ 3 bị hết kho trong lúc đang chạy dở), hệ thống sẽ kích hoạt lệnh `rollback` để khôi phục kho của món hàng thứ 1 và thứ 2 về nguyên trạng, ngăn chặn tuyệt đối tình trạng sai lệch kho.
* **Thống kê gom nhóm nâng cao (Grouped Statistics):** Hệ thống tự động thực hiện các câu lệnh truy vấn phức tạp kết hợp hàm tổng hợp (`SUM`, `COUNT`) và mệnh đề `GROUP BY product_id` để phân tích lịch sử bán hàng. Từ đó, chương trình tự động tính toán chính xác tổng doanh thu, tổng số đơn và tìm ra **Top 3 sản phẩm bán chạy nhất** dựa trên tổng sản lượng đã xuất kho.

## 3. Sắp xếp & Định dạng Dữ liệu Bền vững
* **Sắp xếp đa hình (Polymorphic Sorting):** Tính năng sắp xếp các sản phẩm theo giá bán giảm dần không sử dụng các câu lệnh rẽ nhánh `if-else` thủ công để kiểm tra loại sản phẩm. Thay vào đó, thuật toán tận dụng triệt để tính **Đa hình động**. Khi hàm sắp xếp duyệt qua danh sách, mỗi đối tượng `Laptop`, `Phone`, hay `Fridge` sẽ tự động gọi phương thức `calculate_final_price()` của riêng mình (Laptop cộng 10% thuế linh kiện, Phone cộng 5% phí môi trường, Fridge cộng phí cồng kềnh) để làm tiêu chí xếp hạng.
* **Cơ sở dữ liệu SQLite:** Toàn bộ vòng đời dữ liệu được lưu trữ trong tệp tin quan hệ `store.db`. Dữ liệu không bị mất đi khi tắt chương trình, loại bỏ hoàn toàn nhược điểm ghi đè thủ công của file TXT hay JSON thông thường.
* **Xuất tệp cấu trúc CSV:** Hệ thống hỗ trợ tính năng kết xuất dữ liệu báo cáo kinh doanh ra file `sales_report.csv`. Mã nguồn sử dụng thư viện `csv` kết hợp cấu hình mã hóa mã `utf-8-sig` giúp Thầy giáo khi mở file trực tiếp bằng Microsoft Excel sẽ thấy font chữ Tiếng Việt hiển thị đẹp đẽ, hoàn hảo mà không bị lỗi ký tự.

---

# III. KIẾN TRÚC PHÂN TẦNG CỦA MÃ NGUỒN (LAYERED ARCHITECTURE)

Dự án được phân tách nghiêm ngặt thành **3 tầng độc lập (3-Tier Layered Architecture)** nhằm đảm bảo tính dễ bảo trì, dễ mở rộng và cô lập lỗi:

```text
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


# V. BẢNG TỰ CHẤM ĐIỂM (CRITERIA EVALUATION MATRIX)

Dưới đây là bảng đối chiếu chi tiết giữa barem yêu cầu đạt điểm tuyệt đối (10.0/10.0) của học phần Phương pháp lập trình do Thầy Long phụ trách và cách thức triển khai thực tế trong mã nguồn dự án của em:

| Thành phần (Component) | Tiêu chí chi tiết chấm điểm | Giải thích cơ chế & Cách thức thực hiện chi tiết trong mã nguồn dự án | Trạng thái | Điểm tự chấm |

| :--- | :--- | :--- | :---: | :---: |

| **1. CLI Menu System** | Menu tương tác dùng vòng lặp vô hạn, xử lý lỗi nhập liệu, giao diện có định dạng khung bảng màu sắc ANSI. | Triển khai tại hàm `MenuView.run()` dùng vòng lặp `while True`. Sử dụng các biến mã màu ANSI tiêu chuẩn như `\033[95m` (Tím), `\033[92m` (Xanh lá) để nhuộm màu giao diện. Nếu người dùng nhập sai ký tự lựa chọn, khối `else` sẽ báo lỗi và đẩy menu lặp lại liên tục chứ không sập app. | ✅ Đạt | **1.0 / 1.0** |
| **2. Data Input & Validation** | Thêm bản ghi mới, kiểm tra và ràng buộc dữ liệu đầu vào không cho phép nhập sai kiểu dữ liệu hoặc giá trị âm. | Trong hàm `add_product_menu()`, toàn bộ các lệnh ép kiểu `float()` và `int()` cho Giá và Số lượng được bao bọc trong khối `try-except ValueError` để chặn người dùng nhập chữ. Đồng thời, tại file `models/product.py`, hàm `@base_price.setter` tích hợp logic chặn dữ liệu âm `if value < 0: raise ValueError(...)`. | ✅ Đạt | **1.0 / 1.0** |
| **3. Data Display** | In danh sách bản ghi rõ ràng, căn lề chuẩn xác theo dạng bảng, có tính năng bổ trợ thông minh. | Triển khai tại hàm `MenuView.view_products()`. Sử dụng cú pháp `f-string` định dạng độ rộng cột cố định (`{p.name:<22}`, `{final_price:<15}`) giúp các đường biên bảng `\|` thẳng hàng tuyệt đối. Tích hợp tính năng đổi màu text sang màu Đỏ kèm chữ `(Hết)` nếu tồn kho bằng 0 để cảnh báo thủ kho. | ✅ Đạt | **1.0 / 1.0** |
| **4. Basic Search** | Tìm kiếm bản ghi theo ID hoặc theo tên chính xác / gần đúng chuỗi con. | Triển khai tại hàm `StoreService.search_by_name(keyword)`. Mã nguồn không dùng vòng lặp kiểm tra thủ công mà truyền từ khóa xuống tầng DB, sử dụng truy vấn SQL: `SELECT * FROM products WHERE name LIKE ?` kết hợp tham số `%keyword%` để thực hiện thuật toán tìm kiếm chuỗi con (Substring Search). | ✅ Đạt | **1.0 / 1.0** |
| **5. Sorting Mechanism** | Sắp xếp danh sách theo ít nhất một trường dữ liệu (Giá bán giảm dần) áp dụng tư duy lập trình tối ưu. | Triển khai tại hàm `StoreService.sort_by_price_desc()`. Hàm kết hợp hàm `sorted()` của Python và sử dụng tham số `key=lambda p: p.calculate_final_price()`. Cơ chế này tận dụng tính **Đa hình động**, mỗi đối tượng con tự tính giá bán thực tế sau thuế/phí để làm mốc so sánh sắp xếp. | ✅ Đạt | **1.0 / 1.0** |
| **6. Basic Calculation** | Tính toán thống kê dữ liệu cơ bản từ hệ thống (Tính tổng, tính đếm). | Triển khai tại hàm `InvoiceService.get_revenue_report()`. Hệ thống thực hiện câu lệnh SQL tổng hợp kết hợp các hàm toán học: `SELECT SUM(final_total) as total_revenue, COUNT(*) as total_invoices FROM invoices` để tính toán chính xác dòng tiền thu về của siêu thị. | ✅ Đạt | **1.0 / 1.0** |
| **7. Architecture & Clean Code** | Áp dụng cấu trúc phân tầng (Layered Architecture), mã nguồn sạch tuân thủ quy chuẩn viết code quốc tế. | Dự án chia tách độc lập thành 3 thư mục tầng rõ rệt: `models/` (Định nghĩa thực thể), `services/` (Xử lý logic và SQL), `views/` (Hiển thị CLI). Toàn bộ tên biến, tên hàm viết theo chuẩn `snake_case`, tên lớp viết theo chuẩn `CamelCase` tuân thủ nghiêm ngặt quy định định dạng **PEP 8** của Python. | ✅ Đạt | **1.0 / 1.0** |
| **8. [Advanced] Complex Logic** | Xử lý logic nghiệp vụ nâng cao phức tạp (Logic Giao dịch - Transaction & Đảm bảo tính nhất quán dữ liệu). | Triển khai tại hàm `InvoiceService.create_invoice(cart)`. Quản lý một chuỗi hành động phức tạp lồng nhau: Duyệt kiểm kho -> Thêm hóa đơn -> Thêm chi tiết đơn -> Trừ kho đồng loạt. Chuỗi lệnh được bọc trong bộ quản lý kết nối SQLite, gọi lệnh `conn.commit()` khi thành công và gọi `conn.rollback()` để hoàn kho ngay lập tức nếu xảy ra lỗi thiếu hàng. | ✅ Đạt | **1.0 / 1.0** |
| **9. [Advanced] DBMS Storage** | Nâng cấp hệ thống lưu trữ dữ liệu bền vững sử dụng Hệ quản trị cơ sở dữ liệu quan hệ (DBMS). | Thay vì dùng file TXT thô sơ, dự án tích hợp hệ quản trị cơ sở dữ liệu quan hệ **SQLite** (`store.db`). Thiết lập cấu trúc cơ sở dữ liệu chuẩn hóa gồm 3 bảng quan hệ chặt chẽ, sử dụng ràng buộc Khóa chính (`PRIMARY KEY`) và Khóa ngoại (`FOREIGN KEY ... REFERENCES`) để đảm bảo toàn vẹn tham chiếu. | ✅ Đạt | **1.0 / 1.0** |
| **10. Git, CSV & OOP Capstone** | Sử dụng Git/GitHub, viết README hướng dẫn, áp dụng OOP đầy đủ (Đóng gói, Kế thừa, Trừu tượng) và xuất báo cáo CSV. | Mã nguồn đẩy lên GitHub với lịch sử commit chia nhỏ rõ ràng theo chuẩn `conventional commits`. Sử dụng trọn vẹn 4 tính chất OOP (Trừu tượng qua `ABC`, Đóng gói thuộc tính `__private`, Kế thừa từ lớp `Product`). Hàm `export_sales_report_csv()` xuất bảng dữ liệu cấu trúc ra file CSV hỗ trợ hiển thị Excel tiếng Việt tuyệt đối. | ✅ Đạt | **1.0 / 1.0** |
| **TỔNG CỘNG** | *(Dự án đáp ứng xuất sắc toàn bộ barem điểm tối đa của môn học)* | | | **10.0 / 10.0** |
