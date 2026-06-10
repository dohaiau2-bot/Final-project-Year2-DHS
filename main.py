from services.database import Database
from services.store_service import StoreService
from services.invoice_service import InvoiceService
from views.menu_view import MenuView

def main():
    # Bước 1: Khởi tạo kết nối CSDL SQLite độc lập
    db = Database()
    
    # Bước 2: Tách nhỏ các dịch vụ logic (Tách Store và Invoice riêng biệt theo SRP)
    store_service = StoreService(db)
    invoice_service = InvoiceService(db, store_service)
    
    # Bước 3: Đẩy các service vào điều phối ở view (Dependency Injection)
    ui_menu = MenuView(store_service, invoice_service)
    ui_menu.run()

if __name__ == "__main__":
    main()