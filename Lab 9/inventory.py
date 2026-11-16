from product import Product
class Inventory():
    def __init__(self, products: list[Product] | None = None):
        self.__products: list[Product] = products if products is not None else []
    def add_product(self, product: Product) -> None:
        self.__products.append(product)
    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_id() == product_id:
                return product
        return None
    def search_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            print("\nProduct not found.\n")
            return None
        print("\nProduct Found:")
        print("------------------------------------------------")
        product.display_information_nice()
        print("------------------------------------------------\n")
        return product
    def shipping_information(self, product_id: str) -> None:
        product = self.search_product(product_id)
        if product is None:
            return
        print(product.get_fulfilment_info())
        print("")
    def display_all(self) -> None:
        print("\nCurrent Inventory\n------------------------------------------------")
        if len(self.__products) == 0:
            print("No products found")
        else:
            for product in self.__products:
                product.display_information()
        print("------------------------------------------------\n")
    def get_current_number_of_products(self) -> int:
        return len(self.__products)
    def generate_next_id(self) -> str:
        highest = 0
        for product in self.__products:
            number = product.get_id()[1:]
            if number.isdigit():
                highest = max(highest, int(number))
        return f"P{highest + 1:03d}"
    def print_product_ids(self) -> bool:
        if len(self.__products) == 0:
            print("There are currently no products.\n")
            return False
        for product in self.__products:
            print(product.get_id(), end="|")
        print("\n")
        return True
    def update_inventory_stock(self, product_id: str, quantity: int) -> None:
        product = self.find_product(product_id)
        if product is not None:
            product.update_stock(quantity)
    def get_inventory(self) -> list[Product]:
        return list(self.__products)
