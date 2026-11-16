import json
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
class FileSystem():
    def __init__(self):
        self.__filename: str = 'inventory.json'
    def save_inventory(self, inventory: list[Product]) -> None:
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump([p.to_dict() for p in inventory], file)
    def load_inventory(self) -> list[Product]:
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("inventory.json not found.")
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump([], file)
            print("inventory.json created.")
            print("Created Inventory successfully.\n")
            return []
        print("inventory.json found.")
        print("Inventory loaded successfully.\n")
        return [self.create_product(d) for d in data]
    @staticmethod
    def create_product(d: dict) -> Product:
        PRODUCT_TYPES = {"physical": PhysicalProduct, "digital": DigitalProduct}
        return PRODUCT_TYPES[d["type"]].from_dict(d)
