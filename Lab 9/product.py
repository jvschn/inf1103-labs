from abc import ABC, abstractmethod
from supplier import Supplier
class Product(ABC):
    def __init__(self, id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id: str = id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier
    def to_dict(self) -> dict:
        return {"id": self.__product_id, "name": self.__name, "price": self.__price, "stock": self.__stock, "supplier": self.__supplier.to_dict()}
    @classmethod
    @abstractmethod
    def from_dict(cls, d: dict) -> "Product":
        pass
    def update_stock(self, quantity: int) -> None:
        if quantity >= 0:
            self.__stock = quantity
    def display_information(self, end: str = "\n") -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock} | Supplier: {self.__supplier.get_name()}", end=end)
    def display_information_nice(self) -> None:
        print(f"ID: {self.__product_id}\nName: {self.__name}\nPrice: ${self.__price:.2f}\nStock: {self.__stock}")
        self.__supplier.display_information()
    def get_id(self) -> str:
        return self.__product_id
    def get_name(self) -> str:
        return self.__name
    def get_price(self) -> float:
        return self.__price
    def get_stock(self) -> int:
        return self.__stock
    def get_supplier(self) -> Supplier:
        return self.__supplier
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
