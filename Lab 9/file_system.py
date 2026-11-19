import json
from product import Product
from product_factory import ProductFactory
from supplier import Supplier
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
        except json.JSONDecodeError:
            print("inventory.json is not valid JSON. Starting with an empty inventory.\n")
            return []
        print("inventory.json found.")
        products: list[Product] = []
        for d in data:
            try:
                products.append(self.create_product(d))
            except KeyError as e:
                print(f"Skipped a product with missing field {e} in inventory.json")
            except ValueError as e:
                print(f"Skipped an invalid product in inventory.json: {e}")
        print("Inventory loaded successfully.\n")
        return products
    @staticmethod
    def create_product(d: dict) -> Product:
        return ProductFactory.create(d["type"], d["id"], d["name"], d["price"], d["stock"],
                                     Supplier.from_dict(d["supplier"]),
                                     weight=d.get("weight", 0.0), download_size=d.get("download_size", 0.0))
