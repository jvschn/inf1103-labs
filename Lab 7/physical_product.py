from product import Product
from can_be_shipped import CanBeShipped
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