from product import Product
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