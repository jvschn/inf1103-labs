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

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        return

class PhysicalProduct(Product,CanBeShipped):
    def __init__(self, id, name, price, stock,weight):
        super().__init__(id, name, price, stock)
        self.__weight = weight
    def display_information(self):
        super().display_information(end="")
        print(f" | Weight: {self.__weight}kg")
    def display_information_nice(self):
        super().display_information_nice()
        print(f"Weight: {self.__weight}kg")
    def get_fulfilment_info(self):
        return f"This product has to be shipped."
    def calculate_shipping_cost(self):
        return round(5.00 + 2.00 * self.__weight, 2)
    def to_dict(self):
        d =  super().to_dict()
        d["type"] = "physical"
        d["weight"] = self.__weight
        return d
    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["name"], d["price"], d["stock"], d["weight"])
    

class DigitalProduct(Product):
    def __init__(self, id, name, price, stock,download_size):
        super().__init__(id, name, price, stock)
        self.__download_size = download_size
    def display_information(self):
        super().display_information(end="")
        print(f" | Download Size: {self.__download_size}mb")
    def display_information_nice(self):
        super().display_information_nice()
        print(f"Download Size: {self.__download_size}mb")
    def get_fulfilment_info(self):
        return f"This product has to be downloaded."
    def to_dict(self):
        d =  super().to_dict()
        d["type"] = "digital"
        d["download_size"] = self.__download_size
        return d
    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["name"], d["price"], d["stock"], d["download_size"])


