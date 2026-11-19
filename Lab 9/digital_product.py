from product import Product
from supplier import Supplier
class DigitalProduct(Product):
    def __init__(self, id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier):
        super().__init__(id, name, price, stock, supplier)
        self.__download_size: float = download_size
    def display_information(self) -> None:
        super().display_information(end="")
        print(f" | Download Size: {self.__download_size}mb")
    def display_information_nice(self) -> None:
        super().display_information_nice()
        print(f"Download Size: {self.__download_size}mb")
    def get_fulfilment_info(self) -> str:
        return f"This product has to be downloaded."
    def to_dict(self) -> dict:
        d =  super().to_dict()
        d["type"] = "digital"
        d["download_size"] = self.__download_size
        return d
