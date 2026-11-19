from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier
class PhysicalProduct(Product,CanBeShipped):
    def __init__(self, id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier):
        super().__init__(id, name, price, stock, supplier)
        self.__weight: float = weight
    def display_information(self) -> None:
        super().display_information(end="")
        print(f" | Weight: {self.__weight}kg")
    def display_information_nice(self) -> None:
        super().display_information_nice()
        print(f"Weight: {self.__weight}kg")
    def get_fulfilment_info(self) -> str:
        return f"This product has to be shipped. Shipping cost based on weight($5 + $2/kg): ${self.calculate_shipping_cost():.2f}"
    def calculate_shipping_cost(self) -> float:
        return round(5.00 + 2.00 * self.__weight, 2)
    def to_dict(self) -> dict:
        d =  super().to_dict()
        d["type"] = "physical"
        d["weight"] = self.__weight
        return d
