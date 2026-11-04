import json
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
class FileSystem():
    def __init__(self):
        self.__filename = 'inventory.json'
    def save_inventory(self,inventory):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump([p.to_dict() for p in inventory], file)
    def load_inventory(self):
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print("inventory.json found.")
            print("Inventory loaded successfully.\n")
            return [self.create_product(d) for d in data]
        except:
            print("inventory.json not found.")
            data = []
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data, file)
            print("inventory.json created.")
            print("Created Inventory successfully.\n")
            return []
    @staticmethod
    def create_product(d):
        PRODUCT_TYPES = {"physical": PhysicalProduct, "digital": DigitalProduct}
        return PRODUCT_TYPES[d["type"]].from_dict(d)