from services.store_service import StoreService
from services.invoice_service import InvoiceService
from models.product import Laptop, Phone, Fridge

# Định nghĩa các mã màu ANSI tiêu chuẩn
CLR_HEADER  = "\033[95m"   # Tím sáng (Cho tiêu đề chính)
CLR_MENU    = "\033[94m"   # Xanh dương (Cho các tùy chọn menu)
CLR_SUCCESS = "\033[92m"   # Xanh lá (Cho thông báo thành công)
CLR_WARN    = "\033[93m"   # Vàng (Cho cảnh báo/lưu ý)
CLR_ERROR   = "\033[91m"   # Đỏ (Cho thông báo lỗi nguy hiểm)
CLR_INFO    = "\033[96m"   # Xanh ngọc (Cho bảng biểu/thông tin phụ)
CLR_RESET   = "\033[0m"    # Reset về màu mặc định của Terminal
CLR_BOLD    = "\033[1m"    # In đậm

class MenuView:
    def __init__(self, store_service: StoreService, invoice_service: InvoiceService):
        self.store_service = store_service
        self.invoice_service = invoice_service

    def display_menu(self):
        # Thiết kế menu có khung màu sắc đồng bộ
        print("\n" + CLR_HEADER + "="*60 + CLR_RESET)
        print(CLR_HEADER + CLR_BOLD + "   HỆ THỐNG SIÊU THỊ ĐIỆN MÁY - SQLITE & TRANSACTION" + CLR_RESET)
        print(CLR_HEADER + "="*60 + CLR_RESET)
        print(f"{CLR_MENU} 1.{CLR_RESET} Xem danh sách sản phẩm hiện có")
        print(f"{CLR_MENU} 2.{CLR_RESET} Thêm mới mặt hàng vào kho")
        print(f"{CLR_MENU} 3.{CLR_RESET} Cập nhật số lượng tồn kho lẻ")
        print(f"{CLR_MENU} 4.{CLR_RESET} Xóa sản phẩm khỏi hệ thống")
        print(f"{CLR_MENU} 5.{CLR_RESET} Tìm kiếm sản phẩm theo từ khóa tên")
        print(f"{CLR_MENU} 6.{CLR_RESET} Sắp xếp sản phẩm theo giá bán giảm dần")
        print(f"{CLR_MENU} 7.{CLR_RESET} Giao dịch mua hàng (Tạo Hóa đơn Transaction)")
        print(f"{CLR_MENU} 8.{CLR_RESET} Thống kê kinh doanh & Top bán chạy")
        print(f"{CLR_MENU} 9.{CLR_RESET} Xuất báo cáo doanh số bán hàng (CSV)")
        print(f"{CLR_WARN} 0.{CLR_RESET} Thoát hệ thống")
        print(CLR_HEADER + "="*60 + CLR_RESET)

    def run(self):
        while True:
            self.display_menu()
            choice = input(CLR_BOLD + "Nhập lựa chọn của bạn (0-9): " + CLR_RESET).strip()
            print(CLR_INFO + "-" * 60 + CLR_RESET)
            
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
                    print(f"\n{CLR_HEADER}{CLR_BOLD}--- SẢN PHẨM PHÂN LOẠI THEO GIÁ GIẢM DẦN (ĐA HÌNH) ---{CLR_RESET}")
                    self.view_products(self.store_service.sort_by_price_desc())
                elif choice == "7":
                    self.purchase_menu()
                elif choice == "8":
                    self.statistics_menu()
                elif choice == "9":
                    path = self.invoice_service.export_sales_report_csv()
                    print(f"{CLR_SUCCESS}🎉 Xuất báo cáo thành công tốt đẹp! File lưu tại: {path}{CLR_RESET}")
                elif choice == "0":
                    print(f"{CLR_SUCCESS}Hệ thống đã đóng và bảo mật dữ liệu SQLite an toàn. Tạm biệt!{CLR_RESET}")
                    break
                else:
                    print(f"{CLR_WARN}⚠️ Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 9.{CLR_RESET}")
            except Exception as e:
                print(f"{CLR_ERROR}❌ Đã xảy ra lỗi thực thi hệ thống: {e}{CLR_RESET}")

    def view_products(self, product_list):
        if not product_list:
            print(f"{CLR_WARN}Hiện tại không có sản phẩm nào trong kho dữ liệu.{CLR_RESET}")
            return
        
        # Định dạng Header của bảng bằng màu Xanh Ngọc + In đậm
        print(CLR_INFO + CLR_BOLD + f"{'Mã SP':<7} | {'Tên Sản Phẩm':<22} | {'Loại':<7} | {'Giá Bán':<15} | {'Tồn':<5} | {'Thông số kỹ thuật'}" + CLR_RESET)
        print(CLR_INFO + "-" * 95 + CLR_RESET)
        
        for p in product_list:
            final_price = f"{p.calculate_final_price():,.0f} Đ"
            p_type = p.__class__.__name__
            
            # Đổi màu chữ của Loại sản phẩm để bảng nhìn phân cấp rõ ràng
            type_color = CLR_RESET
            if p_type == "Laptop": type_color = "\033[35m"  # Tím thường
            elif p_type == "Phone": type_color = "\033[32m"  # Xanh lá thường
            elif p_type == "Fridge": type_color = "\033[33m" # Vàng thường

            # Cảnh báo màu đỏ nếu số lượng tồn kho hết hàng (stock == 0)
            stock_str = str(p.stock)
            if p.stock == 0:
                stock_str = f"{CLR_ERROR}0 (Hết){CLR_RESET}"
            elif p.stock <= 3:
                stock_str = f"{CLR_WARN}{p.stock} (Ít){CLR_RESET}"

            # In từng dòng dữ liệu căn lề thẳng thớm
            print(f"{CLR_BOLD}{p.product_id:<7}{CLR_RESET} | {p.name:<22} | {type_color}{p_type:<7}{CLR_RESET} | {CLR_SUCCESS}{final_price:<15}{CLR_RESET} | {stock_str:<5} | {p.get_specs()}")
        print(CLR_INFO + "-" * 95 + CLR_RESET)

    def add_product_menu(self):
        while True:
            print(f"Chọn loại sản phẩm thêm mới: {CLR_MENU}1. Laptop{CLR_RESET} | {CLR_MENU}2. Phone{CLR_RESET} | {CLR_MENU}3. Fridge{CLR_RESET}")
            p_type = input("Nhập (1-3): ").strip()
            if p_type in ["1", "2", "3"]: break
            print(f"{CLR_WARN}⚠️ Sai cú pháp lệnh, mời nhập lại.\n{CLR_RESET}")

        p_id = input("Mã sản phẩm (Ví dụ: L01, P01): ").strip()
        name = input("Tên sản phẩm: ").strip()
        
        try:
            base_price = float(input("Giá nhập gốc (VNĐ): "))
            stock = int(input("Số lượng nhập kho đầu kỳ: "))
            warranty = int(input("Hạn bảo hành (Tháng): "))
        except ValueError:
            print(f"{CLR_ERROR}⚠️ Dữ liệu đầu vào (Giá, số lượng, bảo hành) bắt buộc phải là số!{CLR_RESET}")
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
                print(f"{CLR_ERROR}⚠️ Dung tích phải là chữ số nguyên!{CLR_RESET}")
                return
            new_p = Fridge(p_id, name, base_price, stock, warranty, capacity)

        if self.store_service.add_product(new_p):
            print(f"{CLR_SUCCESS}🎉 Thêm mặt hàng vào cơ sở dữ liệu SQLite thành công!{CLR_RESET}")
        else:
            print(f"{CLR_ERROR}❌ Thất bại! Mã hàng hóa này đã tồn tại sẵn trong hệ thống.{CLR_RESET}")

    def update_stock_menu(self):
        p_id = input("Nhập mã sản phẩm cần đổi số lượng kho: ").strip()
        try:
            new_stock = int(input("Số lượng tồn mới: "))
            if self.store_service.update_product_stock(p_id, new_stock):
                print(f"{CLR_SUCCESS}🎉 Cập nhật cơ sở dữ liệu thành công!{CLR_RESET}")
            else:
                print(f"{CLR_ERROR}❌ Không tìm thấy mã sản phẩm này trong kho.{CLR_RESET}")
        except ValueError as e:
            print(f"{CLR_ERROR}⚠️ Lỗi: {e}{CLR_RESET}")

    def delete_product_menu(self):
        p_id = input("Nhập mã sản phẩm muốn loại bỏ: ").strip()
        confirm = input(f"{CLR_WARN}Xác nhận xóa vĩnh viễn {p_id} khỏi SQLite? (y/n): {CLR_RESET}").strip().lower()
        if confirm == 'y':
            if self.store_service.delete_product(p_id):
                print(f"{CLR_SUCCESS}🎉 Đã xóa sản phẩm thành công.{CLR_RESET}")
            else:
                print(f"{CLR_ERROR}❌ Thất bại! Không tìm thấy mã sản phẩm.{CLR_RESET}")

    def search_menu(self):
        kw = input("Nhập tên hàng hóa cần tìm: ").strip()
        print(f"\n{CLR_HEADER}🔍 Kết quả tìm kiếm cho từ khóa '{kw}':{CLR_RESET}")
        self.view_products(self.store_service.search_by_name(kw))

    def purchase_menu(self):
        print(f"\n{CLR_HEADER}{CLR_BOLD}--- TẠO PHIÊN GIAO DỊCH (TRANSACTION MUA HÀNG) ---{CLR_RESET}")
        cart = {}
        while True:
            p_id = input("Nhập mã sản phẩm khách chọn mua (Enter để kết thúc): ").strip()
            if not p_id: break
            try:
                qty = int(input(f"Số lượng mua cho mặt hàng {p_id}: "))
                if qty <= 0:
                    print(f"{CLR_WARN}⚠️ Số lượng mua phải lớn hơn 0!{CLR_RESET}")
                    continue
                cart[p_id] = cart.get(p_id, 0) + qty
            except ValueError:
                print(f"{CLR_ERROR}⚠️ Vui lòng nhập số nguyên hợp lệ!{CLR_RESET}")

        if not cart:
            print(f"{CLR_WARN}Hủy phiên giao dịch vì giỏ hàng trống.{CLR_RESET}")
            return

        discount_code = input("Mã Voucher giảm giá (Gợi ý: SIEUTHI2026): ").strip()
        
        try:
            invoice = self.invoice_service.create_invoice(cart, discount_code)
            
            # In hóa đơn có viền trang trí màu sắc bắt mắt
            print("\n" + CLR_WARN + "*"*50 + CLR_RESET)
            print(f"{CLR_WARN}{CLR_BOLD} HÓA ĐƠN ĐIỆN TỬ - Số: #{invoice.invoice_id} | Ngày: {invoice.created_at}{CLR_RESET}")
            print(CLR_WARN + "*"*50 + CLR_RESET)
            for item in invoice.items:
                print(f"- {item.product_name:<20} (SL: {item.quantity:<2}) | Đơn giá: {CLR_SUCCESS}{item.unit_price:,.0f} Đ{CLR_RESET}")
            print(CLR_INFO + "-" * 50 + CLR_RESET)
            print(f"Tổng tiền hàng:   {invoice.subtotal:,.0f} VNĐ")
            print(f"Mã giảm giá áp:  {CLR_ERROR}-{invoice.discount:,.0f} VNĐ{CLR_RESET}")
            print(f"{CLR_BOLD}THÀNH TIỀN:       {CLR_SUCCESS}{invoice.final_total:,.0f} VNĐ{CLR_RESET}")
            print(CLR_WARN + "*"*50 + CLR_RESET)
            print(f"{CLR_SUCCESS}🚀 Transaction thành công! Đã trừ tồn kho và đồng bộ hóa SQLite.{CLR_RESET}")
        except ValueError as e:
            print(f"{CLR_ERROR}❌ Giao dịch thất bại: {e}{CLR_RESET}")

    def statistics_menu(self):
        print("\n" + CLR_HEADER + "·"*15 + " BÁO CÁO THỐNG KÊ KINH DOANH " + "·"*15 + CLR_RESET)
        rep = self.invoice_service.get_revenue_report()
        print(f"▪️ Tổng doanh số thu về: {CLR_SUCCESS}{CLR_BOLD}{rep['total_revenue']:,.0f} VNĐ{CLR_RESET}")
        print(f"▪️ Lượng hóa đơn giao dịch: {CLR_INFO}{rep['total_invoices']}{CLR_RESET} đơn")
        print(f"▪️ Số lượng hàng hóa đã xuất kho: {CLR_INFO}{rep['total_items_sold']}{CLR_RESET} sản phẩm")
        
        print(f"\n{CLR_HEADER}{CLR_BOLD}--- TOP 3 SẢN PHẨM BÁN CHẠY NHẤT ---{CLR_RESET}")
        top_items = self.invoice_service.get_top_selling_products(limit=3)
        if not top_items:
            print(f"{CLR_WARN}Chưa có dữ liệu mua hàng để thống kê nhóm.{CLR_RESET}")
            return
        
        print(CLR_INFO + CLR_BOLD + f"{'Xếp hạng':<8} | {'Mã SP':<6} | {'Tên sản phẩm':<20} | {'Loại':<7} | {'Tổng bán':<8} | {'Doanh thu'}" + CLR_RESET)
        print(CLR_INFO + "-" * 80 + CLR_RESET)
        for idx, row in enumerate(top_items, 1):
            print(f"{CLR_WARN}Hạng {idx:<4}{CLR_RESET} | {row['product_id']:<6} | {row['product_name']:<20} | {row['product_type']:<7} | {CLR_BOLD}{row['total_qty']:<8}{CLR_RESET} | {CLR_SUCCESS}{row['total_sales']:,.0f} Đ{CLR_RESET}")