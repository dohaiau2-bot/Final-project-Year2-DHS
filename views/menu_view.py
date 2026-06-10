from services.store_service import StoreService
from services.invoice_service import InvoiceService
from models.product import Laptop, Phone, Fridge

class MenuView:
    def __init__(self, store_service: StoreService, invoice_service: InvoiceService):
        self.store_service = store_service
        self.invoice_service = invoice_service

    def display_menu(self):
        print("\n" + "="*55)
        print("   HỆ THỐNG SIÊU THỊ ĐIỆN MÁY - SQLITE & TRANSACTION")
        print("="*55)
        print("1. Xem danh sách sản phẩm hiện có")
        print("2. Thêm mới mặt hàng vào kho")
        print("3. Cập nhật số lượng tồn kho lẻ")
        print("4. Xóa sản phẩm khỏi hệ thống")
        print("5. Tìm kiếm sản phẩm theo từ khóa tên")
        print("6. Sắp xếp sản phẩm theo giá bán giảm dần")
        print("7. Giao dịch mua hàng (Tạo Hóa đơn Transaction)")
        print("8. Thống kê kinh doanh & Top bán chạy")
        print("9. Xuất báo cáo doanh số bán hàng (CSV)")
        print("0. Thoát hệ thống")
        print("="*55)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Nhập lựa chọn của bạn (0-9): ").strip()
            print("-" * 55)
            
            try:
                if choice == "1":
                    self.view_products(self.store_service.get_all_products())
                elif choice == "2":
                    self.add_product_menu()
                elif choice == "3":
                    self.update_stock_menu()
                elif choice == "4":
                    self.delete_product_menu()
                elif choice == "5":
                    self.search_menu()
                elif choice == "6":
                    print("\n--- SẢN PHẨM PHÂN LOẠI THEO GIÁ GIẢM DẦN (ĐA HÌNH) ---")
                    self.view_products(self.store_service.sort_by_price_desc())
                elif choice == "7":
                    self.purchase_menu()
                elif choice == "8":
                    self.statistics_menu()
                elif choice == "9":
                    path = self.invoice_service.export_sales_report_csv()
                    print(f"🎉 Xuất báo cáo thành công tốt đẹp! File lưu tại: {path}")
                elif choice == "0":
                    print("Hệ thống đã đóng và bảo mật dữ liệu SQLite an toàn. Tạm biệt!")
                    break
                else:
                    print("⚠️ Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 9.")
            except Exception as e:
                print(f"❌ Đã xảy ra lỗi thực thi hệ thống: {e}")

    def view_products(self, product_list):
        if not product_list:
            print("Hiện tại không có sản phẩm nào trong kho dữ liệu.")
            return
        print(f"{'Mã SP':<7} | {'Tên Sản Phẩm':<20} | {'Loại':<7} | {'Giá Bán':<14} | {'Tồn':<4} | {'Thông số kỹ thuật'}")
        print("-" * 90)
        for p in product_list:
            final_price = f"{p.calculate_final_price():,.0f} Đ"
            print(f"{p.product_id:<7} | {p.name:<20} | {p.__class__.__name__:<7} | {final_price:<14} | {p.stock:<4} | {p.get_specs()}")

    def add_product_menu(self):
        while True:
            print("Chọn loại sản phẩm thêm mới: 1. Laptop | 2. Phone | 3. Fridge")
            p_type = input("Nhập (1-3): ").strip()
            if p_type in ["1", "2", "3"]: break
            print("⚠️ Sai cú pháp lệnh, mời nhập lại.\n")

        p_id = input("Mã sản phẩm (Ví dụ: L01, P01): ").strip()
        name = input("Tên sản phẩm: ").strip()
        
        try:
            base_price = float(input("Giá nhập gốc (VNĐ): "))
            stock = int(input("Số lượng nhập kho đầu kỳ: "))
            warranty = int(input("Hạn bảo hành (Tháng): "))
        except ValueError:
            print("⚠️ Dữ liệu đầu vào (Giá, số lượng, bảo hành) bắt buộc phải là số!")
            return

        if p_type == "1":
            ram = input("Dung lượng RAM: ").strip()
            cpu = input("Dòng CPU: ").strip()
            new_p = Laptop(p_id, name, base_price, stock, warranty, ram, cpu)
        elif p_type == "2":
            battery = input("Dung lượng Pin: ").strip()
            camera = input("Độ phân giải Camera: ").strip()
            new_p = Phone(p_id, name, base_price, stock, warranty, battery, camera)
        else:
            try:
                capacity = int(input("Dung tích tủ lạnh (Lít): "))
            except ValueError:
                print("⚠️ Dung tích phải là chữ số nguyên!")
                return
            new_p = Fridge(p_id, name, base_price, stock, warranty, capacity)

        if self.store_service.add_product(new_p):
            print("🎉 Thêm mặt hàng vào cơ sở dữ liệu SQLite thành công!")
        else:
            print("❌ Thất bại! Mã hàng hóa này đã tồn tại sẵn trong hệ thống.")

    def update_stock_menu(self):
        p_id = input("Nhập mã sản phẩm cần đổi số lượng kho: ").strip()
        try:
            new_stock = int(input("Số lượng tồn mới: "))
            if self.store_service.update_product_stock(p_id, new_stock):
                print("🎉 Cập nhật cơ sở dữ liệu thành công!")
            else:
                print("❌ Không tìm thấy mã sản phẩm này trong kho.")
        except ValueError as e:
            print(f"⚠️ Lỗi: {e}")

    def delete_product_menu(self):
        p_id = input("Nhập mã sản phẩm muốn loại bỏ: ").strip()
        confirm = input(f"Xác nhận xóa vĩnh viễn {p_id} khỏi SQLite? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.store_service.delete_product(p_id):
                print("🎉 Đã xóa sản phẩm thành công.")
            else:
                print("❌ Thất bại! Không tìm thấy mã sản phẩm.")

    def search_menu(self):
        kw = input("Nhập tên hàng hóa cần tìm: ").strip()
        self.view_products(self.store_service.search_by_name(kw))

    def purchase_menu(self):
        print("\n--- TẠO PHIÊN GIAO DỊCH GIAO DỊCH (TRANSACTION MUA HÀNG) ---")
        cart = {}
        while True:
            p_id = input("Nhập mã sản phẩm khách chọn mua (Enter để kết thúc): ").strip()
            if not p_id: break
            try:
                qty = int(input(f"Số lượng mua cho mặt hàng {p_id}: "))
                if qty <= 0:
                    print("⚠️ Số lượng mua phải lớn hơn 0!")
                    continue
                cart[p_id] = cart.get(p_id, 0) + qty
            except ValueError:
                print("⚠️ Vui lòng nhập số nguyên hợp lệ!")

        if not cart:
            print("Hủy phiên giao dịch vì giỏ hàng trống.")
            return

        discount_code = input("Mã Voucher giảm giá (Nếu có): ").strip()
        
        try:
            # Thực thi xử lý transaction qua tầng service mới
            invoice = self.invoice_service.create_invoice(cart, discount_code)
            
            print("\n" + "*"*45)
            print(f" HÓA ĐƠN ĐIỆN TỬ - Số: #{invoice.invoice_id} | Ngay: {invoice.created_at}")
            print("*"*45)
            for item in invoice.items:
                print(f"- {item.product_name:<18} (SL: {item.quantity:<2}) | Đơn giá: {item.unit_price:,.0f} Đ")
            print("-" * 45)
            print(f"Tổng tiền hàng:   {invoice.subtotal:,.0f} VNĐ")
            print(f"Mã giảm giá áp:   -{invoice.discount:,.0f} VNĐ")
            print(f"THÀNH TIỀN:       {invoice.final_total:,.0f} VNĐ")
            print("*"*45)
            print("🚀 Transaction thành công! Đã trừ tồn kho và đồng bộ hóa SQLite.")
        except ValueError as e:
            print(f"❌ Giao dịch thất bại: {e}")

    def statistics_menu(self):
        print("\n" + "·"*20 + " BÁO CÁO THỐNG KÊ KINH DOANH " + "·"*20)
        rep = self.invoice_service.get_revenue_report()
        print(f"▪️ Tổng doanh số thu về: {rep['total_revenue']:,.0f} VNĐ")
        print(f"▪️ Lượng hóa đơn giao dịch: {rep['total_invoices']} đơn")
        print(f"▪️ Số lượng hàng hóa đã xuất kho: {rep['total_items_sold']} sản phẩm")
        
        print("\n--- TOP 3 SẢN PHẨM BÁN CHẠY NHẤT ---")
        top_items = self.invoice_service.get_top_selling_products(limit=3)
        if not top_items:
            print("Chưa có dữ liệu mua hàng để thống kê nhóm.")
            return
        
        print(f"{'Xếp hạng':<8} | {'Mã SP':<6} | {'Tên sản phẩm':<18} | {'Loại':<7} | {'Tổng bán':<8} | {'Doanh thu'}")
        print("-" * 75)
        for idx, row in enumerate(top_items, 1):
            print(f"Hạng {idx:<4} | {row['product_id']:<6} | {row['product_name']:<18} | {row['product_type']:<7} | {row['total_qty']:<8} | {row['total_sales']:,.0f} Đ")