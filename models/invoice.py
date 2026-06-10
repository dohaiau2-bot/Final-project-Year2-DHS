from datetime import datetime

class InvoiceItem:
    """Đại diện cho một dòng chi tiết trong hóa đơn"""
    def __init__(self, product_id: str, product_name: str, p_type: str, quantity: int, unit_price: float):
        self.__product_id = product_id
        self.__product_name = product_name
        self.__p_type = p_type
        self.__quantity = quantity
        self.__unit_price = unit_price

    @property
    def product_id(self): return self.__product_id
    @property
    def product_name(self): return self.__product_name
    @property
    def p_type(self): return self.__p_type
    @property
    def quantity(self): return self.__quantity
    @property
    def unit_price(self): return self.__unit_price
    @property
    def total_price(self): return self.__quantity * self.__unit_price


class Invoice:
    """Đại diện cho một hóa đơn bán hàng hoàn chỉnh"""
    def __init__(self, invoice_id: int = None, date_str: str = None, subtotal: float = 0, discount: float = 0, final_total: float = 0):
        self.__invoice_id = invoice_id
        self.__created_at = date_str if date_str else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subtotal = subtotal
        self.discount = discount
        self.final_total = final_total
        self.items = []  # Danh sách các InvoiceItem

    @property
    def invoice_id(self): return self.__invoice_id
    @property
    def created_at(self): return self.__created_at

    def add_item(self, item: InvoiceItem):
        self.items.append(item)