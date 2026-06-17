from services.database import Database
from models.product import Laptop, Phone, Fridge, Product

class StoreService:
    """Quản lý các nghiệp vụ CRUD Sản phẩm tương tác trực tiếp với SQLite"""
    def __init__(self, db: Database):
        self.db = db

    def _row_to_product(self, row) -> Product:
        p_type = row["type"]
        if p_type == "Laptop":
            return Laptop(row["product_id"], row["name"], row["base_price"], row["stock"], row["warranty_months"], row["spec_1"], row["spec_2"])
        elif p_type == "Phone":
            return Phone(row["product_id"], row["name"], row["base_price"], row["stock"], row["warranty_months"], row["spec_1"], row["spec_2"])
        elif p_type == "Fridge":
            return Fridge(row["product_id"], row["name"], row["base_price"], row["stock"], row["warranty_months"], int(row["spec_1"]))
        return None

    def get_all_products(self):
        products = []
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            for row in cursor.fetchall():
                p = self._row_to_product(row)
                if p: products.append(p)
        return products

    def get_product_by_id(self, product_id: str) -> Product:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_product(row)
        return None

    def add_product(self, product: Product) -> bool:
        if self.get_product_by_id(product.product_id):
            return False  # Trùng ID
        
        # Trích xuất dữ liệu đặc trưng dựa trên class con để lưu vào DB phân mảnh chéo
        spec_1, spec_2 = None, None
        p_type = product.__class__.__name__
        
        #  đọc thuộc tính private phục vụ việc lưu trữ database
        dict_data = product.to_dict()
        if p_type == "Laptop":
            spec_1, spec_2 = dict_data["ram"], dict_data["cpu"]
        elif p_type == "Phone":
            spec_1, spec_2 = dict_data["battery"], dict_data["camera"]
        elif p_type == "Fridge":
            spec_1 = dict_data["capacity"]

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (product_id, name, base_price, stock, warranty_months, type, spec_1, spec_2)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (product.product_id, product.name, product.base_price, product.stock, product.warranty_months, p_type, str(spec_1), spec_2))
            conn.commit()
        return True

    def update_product_stock(self, product_id: str, new_stock: int) -> bool:
        if new_stock < 0: raise ValueError("Số lượng tồn kho không được âm!")
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET stock = ? WHERE product_id = ?", (new_stock, product_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_product(self, product_id: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            conn.commit()
            return cursor.rowcount > 0

    def search_by_name(self, keyword: str):
        products = []
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{keyword}%",))
            for row in cursor.fetchall():
                products.append(self._row_to_product(row))
        return products

    def sort_by_price_desc(self):
        # Vì cách tính tiền của bạn mang tính đa hình ở tầng Python (mỗi loại sản phẩm nhân hệ số thuế/phí khác nhau)
        # Chúng ta sẽ lấy toàn bộ danh sách lên rồi thực hiện sort bằng hàm đa hình tương tự bản cũ của bạn.
        all_p = self.get_all_products()
        return sorted(all_p, key=lambda p: p.calculate_final_price(), reverse=True)