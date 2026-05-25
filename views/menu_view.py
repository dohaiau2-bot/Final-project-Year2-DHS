from services.store_service import StoreService
from models.product import Laptop, Phone, Fridge

class MenuView:
    def __init__(self, service: StoreService):
        self.service = service

    def display_menu(self):
        print("\n" + "="*55)
        print("    HỆ THỐNG QUẢN LÝ SIÊU THỊ ĐIỆN MÁY ĐA PHÂN TẦNG")
        print("="*55)
        print("1. Xem danh sách sản phẩm (Bảng định dạng)")
        print("2. Thêm mới sản phẩm (Laptop / Phone / Fridge)")
        print("3. Cập nhật số lượng tồn kho")
        print("4. Xóa sản phẩm")
        print("5. Tìm kiếm sản phẩm theo tên")
        print("6. Sắp xếp sản phẩm theo giá bán giảm dần")
        print("7. Mua hàng (Tạo hóa đơn & Trừ kho)")
        print("8. Xuất báo cáo tồn kho ra file CSV")
        print("0. Thoát chương trình (Tự động lưu)")
        print("="*55)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Nhập lựa chọn của bạn (0-8): ").strip()
            print("-" * 55)
            
            # XỬ LÝ NGOẠI LỆ TOÀN CỤC TRÊN MENU
            try:
                if choice == "1":
                    self.view_products(self.service.get_all_products())
                elif choice == "2":
                    self.add_product_menu()
                elif choice == "3":
                    self.update_stock_menu()
                elif choice == "4":
                    self.delete_product_menu()
                elif choice == "5":
                    self.search_menu()
                elif choice == "6":
                    print("\n--- DANH SÁCH SẢN PHẨM SẮP XẾP GIÁ GIẢM DẦN ---")
                    self.view_products(self.service.sort_by_price_desc())
                elif choice == "7":
                    self.purchase_menu()
                elif choice == "8":
                    path = self.service.export_inventory_report_csv()
                    print(f"🎉 Xuất báo cáo thành công! File lưu tại: {path}")
                elif choice == "0":
                    print("Cảm ơn bạn đã sử dụng hệ thống! Dữ liệu đã được lưu an toàn.")
                    break
                else:
                    print("⚠️ Lựa chọn không hợp lệ, vui lòng chọn lại từ 0 đến 8.")
            except Exception as e:
                print(f"❌ Đã xảy ra lỗi hệ thống: {e}")

    def view_products(self, product_list):
        if not product_list:
            print("Hiện tại không có sản phẩm nào trong hệ thống.")
            return
        
        # In format dạng bảng CLI
        print(f"{'Mã SP':<8} | {'Tên Sản Phẩm':<20} | {'Loại':<8} | {'Giá Bán':<15} | {'Tồn':<5} | {'Thông số / Tiện ích'}")
        print("-" * 90)
        for p in product_list:
            final_price = f"{p.calculate_final_price():,.0f} Đ"
            print(f"{p.product_id:<8} | {p.name:<20} | {p.__class__.__name__:<8} | {final_price:<15} | {p.stock:<5} | {p.get_specs()}")

    def add_product_menu(self):
        print("Chọn loại sản phẩm cần thêm:")
        print("1. Laptop | 2. Phone | 3. Fridge")
        p_type = input("Nhập (1-3): ").strip()
        
        if p_type not in ["1", "2", "3"]:
            print("⚠️ Loại sản phẩm không hợp lệ.")
            return

        p_id = input("Nhập mã sản phẩm (Ví dụ: L01, P01): ").strip()
        name = input("Nhập tên sản phẩm: ").strip()
        
        # Bắt lỗi nhập số (Validation logic)
        try:
            base_price = float(input("Nhập giá gốc (VNĐ): "))
            stock = int(input("Nhập số lượng nhập kho: "))
            warranty = int(input("Nhập số tháng bảo hành: "))
        except ValueError:
            print("⚠️ Lỗi dữ liệu: Giá, số lượng và bảo hành phải là ký tự số!")
            return

        if p_type == "1":
            ram = input("Nhập RAM (Ví dụ: 16GB): ").strip()
            cpu = input("Nhập CPU (Ví dụ: Core i7): ").strip()
            new_p = Laptop(p_id, name, base_price, stock, warranty, ram, cpu)
        elif p_type == "2":
            battery = input("Nhập Dung lượng Pin (Ví dụ: 5000mAh): ").strip()
            camera = input("Nhập Thông số Camera (Ví dụ: 108MP): ").strip()
            new_p = Phone(p_id, name, base_price, stock, warranty, battery, camera)
        else:
            try:
                capacity = int(input("Nhập dung tích tủ lạnh (Lít): "))
            except ValueError:
                print("⚠️ Dung tích phải là số nguyên!")
                return
            new_p = Fridge(p_id, name, base_price, stock, warranty, capacity)

        if self.service.add_product(new_p):
            print("🎉 Thêm sản phẩm thành công!")
        else:
            print("❌ Thêm thất bại! Mã sản phẩm đã tồn tại.")

    def update_stock_menu(self):
        p_id = input("Nhập mã sản phẩm cần cập nhật kho: ").strip()
        try:
            new_stock = int(input("Nhập số lượng tồn kho mới: "))
            if self.service.update_product_stock(p_id, new_stock):
                print("🎉 Cập nhật số lượng thành công!")
            else:
                print("❌ Không tìm thấy mã sản phẩm này.")
        except ValueError:
            print("⚠️ Số lượng nhập vào phải là số nguyên!")

    def delete_product_menu(self):
        p_id = input("Nhập mã sản phẩm muốn xóa: ").strip()
        confirm = input(f"Bạn có chắc chắn muốn xóa {p_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.service.delete_product(p_id):
                print("🎉 Đã xóa sản phẩm thành công khỏi hệ thống.")
            else:
                print("❌ Không tìm thấy mã sản phẩm cần xóa.")

    def search_menu(self):
        keyword = input("Nhập tên sản phẩm cần tìm kiếm: ").strip()
        results = self.service.search_by_name(keyword)
        print(f"\n🔍 Kết quả tìm kiếm cho từ khóa '{keyword}':")
        self.view_products(results)

    def purchase_menu(self):
        print("\n--- QUY TRÌNH THANH TOÁN GIAO DỊCH CHỢ ĐIỆN MÁY ---")
        cart = {}
        while True:
            p_id = input("Nhập mã sản phẩm khách mua (hoặc nhấn Enter để dừng chọn): ").strip()
            if not p_id:
                break
            try:
                qty = int(input(f"Nhập số lượng cho mã {p_id}: "))
                if qty <= 0:
                    print("⚠️ Số lượng mua phải lớn hơn 0!")
                    continue
                cart[p_id] = cart.get(p_id, 0) + qty
            except ValueError:
                print("⚠️ Vui lòng nhập số lượng bằng số!")

        if not cart:
            print("Giỏ hàng trống. Hủy giao dịch.")
            return

        discount_code = input("Nhập mã giảm giá nếu có (Gợi ý mã: SIEUTHI2026): ").strip()
        
        try:
            # Gọi service xử lý logic giao dịch phức tạp
            invoice = self.service.create_invoice(cart, discount_code)
            
            print("\n" + "*"*40)
            print("            HÓA ĐƠN BÁN HÀNG")
            print("*"*40)
            for item in invoice["items"]:
                print(f"- {item['name']} (SL: {item['qty']}) | Đơn giá: {item['unit_price']:,.0f} Đ")
            print("-" * 40)
            print(f"Tổng tiền hàng:   {invoice['subtotal']:,.0f} VNĐ")
            print(f"Chiết khấu giảm:  -{invoice['discount']:,.0f} VNĐ")
            print(f"THÀNH TIỀN:       {invoice['final_total']:,.0f} VNĐ")
            print("*"*40)
            print("🚀 Giao dịch thành công! Kho hàng đã được tự động cập nhật.")
        except ValueError as e:
            print(f"❌ Giao dịch thất bại: {e}")