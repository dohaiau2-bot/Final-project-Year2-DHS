import json
import os
import csv
from models.product import Laptop, Phone, Fridge, Product

class StoreService:
    def __init__(self, data_filepath="data/products.json"):
        self.data_filepath = data_filepath
        self.products = []
        self.load_data()

    # LƯU TRỮ VĨNH VIỄN (File I/O JSON)
    def load_data(self):
        if not os.path.exists(self.data_filepath):
            return
        try:
            with open(self.data_filepath, "r", encoding="utf-8") as f:
                data_list = json.load(f)
                for item in data_list:
                    p_type = item["type"]
                    if p_type == "Laptop":
                        p = Laptop(item["product_id"], item["name"], item["base_price"], item["stock"], item["warranty_months"], item["ram"], item["cpu"])
                    elif p_type == "Phone":
                        p = Phone(item["product_id"], item["name"], item["base_price"], item["stock"], item["warranty_months"], item["battery"], item["camera"])
                    elif p_type == "Fridge":
                        p = Fridge(item["product_id"], item["name"], item["base_price"], item["stock"], item["warranty_months"], item["capacity"])
                    self.products.append(p)
        except Exception as e:
            print(f"Lỗi nạp dữ liệu: {e}")

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_filepath), exist_ok=True)
        with open(self.data_filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.products], f, ensure_ascii=False, indent=4)

    # NGHIỆP VỤ CƠ BẢN (CRUD)
    def add_product(self, product: Product) -> bool:
        if any(p.product_id == product.product_id for p in self.products):
            return False  # Trùng ID
        self.products.append(product)
        self.save_data()
        return True

    def get_all_products(self):
        return self.products

    def update_product_stock(self, product_id: str, new_stock: int) -> bool:
        for p in self.products:
            if p.product_id == product_id:
                p.stock = new_stock
                self.save_data()
                return True
        return False

    def delete_product(self, product_id: str) -> bool:
        for p in self.products:
            if p.product_id == product_id:
                self.products.remove(p)
                self.save_data()
                return True
        return False

    # TÌM KIẾM & SẮP XẾP
    def search_by_name(self, keyword: str):
        return [p for p in self.products if keyword.lower() in p.name.lower()]

    def sort_by_price_desc(self):
        # Tính đa hình thể hiện ở đây khi gọi `calculate_final_price()` động cho mọi sản phẩm
        return sorted(self.products, key=lambda p: p.calculate_final_price(), reverse=True)

    # LOGIC GIAO DỊCH PHỨC TẠP (Advanced Transaction Logic)
    def create_invoice(self, cart: dict, discount_code: str = "") -> dict:
        """
        cart: dict { product_id: quantity }
        Xử lý hóa đơn: kiểm tra tồn kho, trừ kho trực tiếp, tính tổng tiền, áp mã giảm giá
        """
        invoice_items = []
        subtotal = 0.0

        # Kiểm tra trước xem có đủ hàng không để tránh trừ kho nửa chừng
        for p_id, qty in cart.items():
            product = next((p for p in self.products if p.product_id == p_id), None)
            if not product:
                raise ValueError(f"Sản phẩm ID {p_id} không tồn tại!")
            if product.stock < qty:
                raise ValueError(f"Sản phẩm {product.name} không đủ hàng! (Còn lại: {product.stock})")

        # Thực hiện trừ kho và tạo chi tiết hóa đơn
        for p_id, qty in cart.items():
            product = next(p for p in self.products if p.product_id == p_id)
            product.stock -= qty
            item_price = product.calculate_final_price()
            item_total = item_price * qty
            subtotal += item_total
            invoice_items.append({
                "id": p_id,
                "name": product.name,
                "qty": qty,
                "unit_price": item_price,
                "total": item_total
            })

        # Áp dụng mã giảm giá
        discount = 0.0
        if discount_code.upper() == "SIEUTHI2026":
            discount = subtotal * 0.10  # Giảm giá 10%

        final_total = subtotal - discount
        self.save_data()  # Đồng bộ lại vào file JSON sau khi trừ kho

        return {
            "items": invoice_items,
            "subtotal": subtotal,
            "discount": discount,
            "final_total": final_total
        }

    # THỐNG KÊ NÂNG CAO & XUẤT CSV (Advanced Statistics & Export)
    def export_inventory_report_csv(self, filepath="data/inventory_report.csv") -> str:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã SP", "Tên Sản Phẩm", "Loại", "Số Lượng Tồn", "Giá Gốc", "Giá Bán Lẻ (Gồm Thuế/Phí)"])
            for p in self.products:
                writer.writerow([
                    p.product_id, 
                    p.name, 
                    p.__class__.__name__, 
                    p.stock, 
                    f"{p.base_price:,.0f} VNĐ", 
                    f"{p.calculate_final_price():,.0f} VNĐ"
                ])
        return filepath