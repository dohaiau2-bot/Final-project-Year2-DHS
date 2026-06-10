import csv
import os
from services.database import Database
from services.store_service import StoreService
from models.invoice import Invoice, InvoiceItem

class InvoiceService:
    """Xử lý Transaction Giao dịch Hóa đơn phức tạp và kết xuất Thống kê báo cáo nhóm"""
    def __init__(self, db: Database, store_service: StoreService):
        self.db = db
        self.store_service = store_service

    # ====== 10. ADVANCED TRANSACTION LOGIC ======
    def create_invoice(self, cart: dict, discount_code: str = "") -> Invoice:
        """
        Thực hiện quy trình transaction an toàn (ACID):
        Kiểm tra kho -> Trừ kho hàng loạt -> Ghi nhận hóa đơn -> Ghi nhận chi tiết hóa đơn.
        Tất cả cuốn chiếu trong cùng 1 Database Connection để tránh xung đột dữ liệu.
        """
        if not cart:
            raise ValueError("Giỏ hàng rỗng!")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            invoice_items_to_create = []
            subtotal = 0.0

            # Bước 1: Kiểm tra tính hợp lệ và số lượng tồn kho của toàn bộ giỏ hàng
            for p_id, qty in cart.items():
                product = self.store_service.get_product_by_id(p_id)
                if not product:
                    raise ValueError(f"Sản phẩm ID {p_id} không tồn tại trên hệ thống!")
                if product.stock < qty:
                    raise ValueError(f"Sản phẩm [{product.name}] không đủ hàng! Hiện còn: {product.stock}")
                
                # Tính giá áp dụng tính Đa hình (Polymorphism)
                final_unit_price = product.calculate_final_price()
                item_total = final_unit_price * qty
                subtotal += item_total

                # Chuẩn bị dữ liệu để insert sau
                invoice_items_to_create.append({
                    "product_id": p_id,
                    "name": product.name,
                    "type": product.__class__.__name__,
                    "qty": qty,
                    "unit_price": final_unit_price
                })

            # Bước 2: Áp dụng mã giảm giá ưu đãi
            discount = 0.0
            if discount_code.upper() == "SIEUTHI2026":
                discount = subtotal * 0.10  # Chiết khấu 10%
            final_total = subtotal - discount

            # Tạo đối tượng Invoice nghiệp vụ
            invoice = Invoice(subtotal=subtotal, discount=discount, final_total=final_total)

            # Bước 3: Ghi dữ liệu vào DB (Thực thi Transaction)
            # 3a. Lưu bảng hóa đơn chính
            cursor.execute("""
                INSERT INTO invoices (created_at, subtotal, discount, final_total)
                VALUES (?, ?, ?, ?)
            """, (invoice.created_at, invoice.subtotal, invoice.discount, invoice.final_total))
            
            invoice_id = cursor.lastrowid # Lấy ID tự sinh của hóa đơn vừa tạo

            # 3b. Lưu bảng chi tiết hóa đơn & Cập nhật trừ kho hàng hóa
            for item in invoice_items_to_create:
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, product_id, product_name, product_type, quantity, unit_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (invoice_id, item["product_id"], item["name"], item["type"], item["qty"], item["unit_price"]))

                # Thực hiện trừ kho sản phẩm trực tiếp trong database
                cursor.execute("""
                    UPDATE products 
                    SET stock = stock - ? 
                    WHERE product_id = ?
                """, (item["qty"], item["product_id"]))

                # Đẩy ngược item vào object invoice để trả về hiển thị ở View
                invoice.add_item(InvoiceItem(item["product_id"], item["name"], item["type"], item["qty"], item["unit_price"]))

            conn.commit()  # Xác nhận mọi thay đổi thành công tốt đẹp
            return invoice

        except Exception as e:
            conn.rollback()  # Quay xe, hủy bỏ toàn bộ thao tác nếu có bất kỳ lỗi gì xảy ra
            raise e
        finally:
            conn.close()

    # ====== 11. ADVANCED STATISTICS & EXPORT ======
    def get_revenue_report() -> dict:
        """Thống kê tổng quan: Tổng doanh thu, số hóa đơn đã bán, tổng số lượng sản phẩm bán ra"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(final_total) FROM invoices")
            inv_count, total_rev = cursor.fetchone()
            
            cursor.execute("SELECT SUM(quantity) FROM invoice_items")
            total_items = cursor.fetchone()[0]
            
            return {
                "total_invoices": inv_count if inv_count else 0,
                "total_revenue": total_rev if total_rev else 0.0,
                "total_items_sold": total_items if total_items else 0
            }

    def get_top_selling_products(self, limit: int = 3):
        """Thống kê nhóm: Tìm Top sản phẩm bán chạy nhất hệ thống"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_id, product_name, product_type, SUM(quantity) as total_qty, SUM(quantity * unit_price) as total_sales
                FROM invoice_items
                GROUP BY product_id, product_name, product_type
                ORDER BY total_qty DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def export_sales_report_csv(self, filepath="data/sales_report.csv") -> str:
        """Xuất báo cáo chi tiết lịch sử giao dịch và doanh số nhóm ra tệp CSV hỗ trợ hiển thị Tiếng Việt"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.invoice_id, i.created_at, ii.product_id, ii.product_name, ii.product_type, ii.quantity, ii.unit_price, (ii.quantity * ii.unit_price) as total
                FROM invoices i
                JOIN invoice_items ii ON i.invoice_id = ii.invoice_id
                ORDER BY i.invoice_id DESC
            """)
            rows = cursor.fetchall()

        with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Mã Hóa Đơn", "Ngày Giao Dịch", "Mã Sản Phẩm", "Tên Sản Phẩm", "Phân Loại", "Số Lượng Bán", "Đơn Giá", "Tổng Tiền (Chưa giảm giá)"])
            for row in rows:
                writer.writerow([
                    row["invoice_id"], row["created_at"], row["product_id"],
                    row["product_name"], row["product_type"], row["quantity"],
                    f"{row['unit_price']:,.0f} VNĐ", f"{row['total']:,.0f} VNĐ"
                ])
        return filepath