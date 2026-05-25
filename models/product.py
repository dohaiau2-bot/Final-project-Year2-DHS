from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id: str, name: str, base_price: float, stock: int, warranty_months: int):
        self.__product_id = product_id
        self.__name = name
        self.base_price = base_price 
        self.stock = stock            
        self.__warranty_months = warranty_months

 
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def base_price(self):
        return self.__base_price

    @base_price.setter
    def base_price(self, value):
        if value < 0:
            raise ValueError("Giá sản phẩm không được âm!")
        self.__base_price = value

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("Số lượng tồn kho không được âm!")
        self.__stock = value

    @property
    def warranty_months(self):
        return self.__warranty_months

    # TRỪU TƯỢNG (Abstraction): Ép buộc các lớp con phải tự định nghĩa cách tính giá riêng
    @abstractmethod
    def calculate_final_price(self) -> float:
        pass

    @abstractmethod
    def get_specs(self) -> str:
        pass

    def to_dict(self) -> dict:
        """Chuyển đổi object thành dictionary để lưu file JSON"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "base_price": self.base_price,
            "stock": self.stock,
            "warranty_months": self.warranty_months,
            "type": self.__class__.__name__
        }


# KẾ THỪA (Inheritance): Laptop kế thừa từ Product
class Laptop(Product):
    def __init__(self, product_id: str, name: str, base_price: float, stock: int, warranty_months: int, ram: str, cpu: str):
        super().__init__(product_id, name, base_price, stock, warranty_months)
        self.__ram = ram
        self.__cpu = cpu

    # ĐA HÌNH (Polymorphism): Laptop tính thêm 10% thuế linh kiện phần cứng cao cấp
    def calculate_final_price(self) -> float:
        return self.base_price * 1.10

    def get_specs(self) -> str:
        return f"RAM: {self.__ram}, CPU: {self.__cpu}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"ram": self.__ram, "cpu": self.__cpu})
        return d


# KẾ THỪA (Inheritance): Phone kế thừa từ Product
class Phone(Product):
    def __init__(self, product_id: str, name: str, base_price: float, stock: int, warranty_months: int, battery: str, camera: str):
        super().__init__(product_id, name, base_price, stock, warranty_months)
        self.__battery = battery
        self.__camera = camera

    # ĐA HÌNH (Polymorphism): Phone chịu thuế môi trường pin điện tử cố định 5%
    def calculate_final_price(self) -> float:
        return self.base_price * 1.05

    def get_specs(self) -> str:
        return f"Pin: {self.__battery}, Camera: {self.__camera}"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"battery": self.__battery, "camera": self.__camera})
        return d


# KẾ THỪA (Inheritance): Fridge kế thừa từ Product
class Fridge(Product):
    def __init__(self, product_id: str, name: str, base_price: float, stock: int, warranty_months: int, capacity: int):
        super().__init__(product_id, name, base_price, stock, warranty_months)
        self.__capacity = capacity

    # ĐA HÌNH (Polymorphism): Tủ lạnh cồng kềnh cộng thêm 200,000đ phí vận chuyển bảo quản
    def calculate_final_price(self) -> float:
        return self.base_price + 200000

    def get_specs(self) -> str:
        return f"Dung tích: {self.__capacity}L"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"capacity": self.__capacity})
        return d