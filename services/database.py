import sqlite3
import os

class Database:
    """Quản lý kết nối và khởi tạo cấu trúc bảng SQLite"""
    def __init__(self, db_path="data/store.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Truy xuất dữ liệu theo tên cột như dict
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Bảng sản phẩm
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    base_price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    warranty_months INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    spec_1 TEXT, -- RAM (Laptop), Battery (Phone), Capacity (Fridge)
                    spec_2 TEXT  -- CPU (Laptop), Camera (Phone)
                )
            """)
            # 2. Bảng hóa đơn
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    discount REAL NOT NULL,
                    final_total REAL NOT NULL
                )
            """)
            # 3. Bảng chi tiết hóa đơn
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id INTEGER NOT NULL,
                    product_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    product_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
                )
            """)
            conn.commit()