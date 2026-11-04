from abc import ABC, abstractmethod
class Product(ABC):
    def __init__(self, id, name, price, stock):
        self.__product_id = id
        self.__name = name
        self.__price = price
        self.__stock = stock
    def to_dict(self):
        return {"id": self.__product_id, "name": self.__name, "price": self.__price, "stock": self.__stock}
    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["name"], d["price"], d["stock"])
    def update_stock(self, quantity):
        if quantity >= 0:
            self.__stock = quantity
    def display_information(self,end="\n"):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}", end=end)
    def display_information_nice(self):
        print(f"ID: {self.__product_id}\nName: {self.__name}\nPrice: ${self.__price:.2f}\nStock: {self.__stock}")
    def get_id(self):
        return self.__product_id
    @abstractmethod
    def get_fulfilment_info(self):
        return