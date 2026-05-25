from services.store_service import StoreService
from views.menu_view import MenuView

def main():
    # 1. Khởi tạo tầng nghiệp vụ (Tự động nạp cơ sở dữ liệu JSON nếu có)
    store_service = StoreService()
    
    # 2. Tiêm service vào tầng hiển thị (Dependency Injection đơn giản)
    ui_menu = MenuView(store_service)
    
    # 3. Chạy chương trình
    ui_menu.run()

if __name__ == "__main__":
    main()