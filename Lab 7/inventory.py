from product import CanBeShipped
class Inventory():
    def __init__(self,inventory):
        self.__inventory = inventory
    def add_product(self,product):
        self.__inventory.append(product)
    def search_product(self,searchid):
        for i in range(len(self.__inventory)):
            if searchid == self.__inventory[i].get_id():
                print("\nProduct Found:")
                print("------------------------------------------------")
                self.__inventory[i].display_information_nice()
                print("------------------------------------------------\n")
                return i
        print("\nProduct not found.\n")
        return 
    def shipping_information(self, searchid):
        i = self.search_product(searchid)
        if i is None:
            return
        product = self.__inventory[i]
        print(product.get_fulfilment_info())
        if isinstance(product, CanBeShipped):
            print(f"Shipping cost based on weight($5 + $2/kg): ${product.calculate_shipping_cost():.2f}")
        print("")
    def display_all(self):
        print("\nCurrent Inventory\n------------------------------------------------")
        if len(self.__inventory) == 0:
            print("No products found")
        else:
            for i in range(len(self.__inventory)):
                self.__inventory[i].display_information()
        print("------------------------------------------------\n")
    def get_current_number_of_products(self):
        return len(self.__inventory)
    def print_product_ids(self):
        if len(self.__inventory) == 0:
            print("There are currently no products.\n")
            return 'error'
        for i in range(len(self.__inventory)):
            print(self.__inventory[i].get_id(),end="|")
        print("\n")
    def update_inventory_stock(self,id,quantity):
        self.__inventory[id].update_stock(quantity)
    def get_inventory(self):
        return self.__inventory