import json

class Product():
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
    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")
    def display_information_nice(self):
        print(f"ID: {self.__product_id}\nName: {self.__name}\nPrice: ${self.__price:.2f}\nStock: {self.__stock}")
    def get_id(self):
        return self.__product_id

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
            return [Product.from_dict(d) for d in data]
        except:
            print("inventory.json not found.")
            data = []
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data, file)
            print("inventory.json created.")
            print("Created Inventory successfully.\n")
            return []

def get_valid_input(user_input,sequence):
    if sequence == "menu":
        try:
            if int(user_input)<1 or int(user_input)>6:
                print("\nPlease only input numbers 1-6.\n")
            else:
                return int(user_input)
        except:
            print("\nPlease only input numbers 1-6.\n")
    elif sequence == "str":
        return user_input
    elif sequence == "int":
        try:
            if int(user_input) <= 0:
                print("Invalid input. Please enter a positive number.\n")
                return 'error'
            else:
                return int(user_input)
        except: 
            print("Invalid input. Please input whole number.\n")
            return 'error'
    elif sequence == "price":
         try:
             if float(user_input) <= 0:
                 print("Invalid input. Please enter a positive number.\n")
                 return 'error'
             else:
                 return float(user_input)
         except: 
             print("Invalid input. Please input a number.\n")
             return 'error'

def exit_programme():
    print("\nSaving inventory before exit...")
    file.save_inventory(inventory.get_inventory())
    print("Inventory saved successfully.\n")
    print("Thank you for using Inventory Management System.\nProgram terminated.")
    return


def menu():
    while True:
        userInput = get_valid_input(input("Enter option: "),"menu")
        if userInput == 1:
            inventory.display_all()
        elif userInput == 2:
            add_product()
            print("Product added successfully!\n")
        elif userInput == 3:
            update_stock()
        elif userInput == 4:
            search_product()
        elif userInput == 5:
            print("\nSaving inventory...")
            file.save_inventory(inventory.get_inventory())
            print("Inventory saved successfully to inventory.json\n")
        elif userInput == 6:
            exit_programme()
            return
        else:
            continue

def add_product():
    newID = f"P{int(inventory.get_current_number_of_products()+1):0{3}d}"
    print("\nAdd New Product")
    print(f"Product ID: {newID}")
    n = 1
    while n < 4:
        if n == 1:
            nameInput = get_valid_input(input("Product Name: "),"str")
            if nameInput != "error":
                n += 1
        elif n ==2:
            costInput = get_valid_input(input("Price: $"),"price")
            if costInput != "error":
                costInput = float("{:.2f}".format(costInput))
                n += 1
        else:
            quantityInput = get_valid_input(input("Stock Quantity: "),"int")
            if quantityInput != "error":
                n += 1
                break
    inventory.add_product(Product(newID,nameInput,costInput,quantityInput))
    return
def search_product():
    if inventory.print_product_ids() != 'error':
        while True:
            userInput = get_valid_input(input("Enter Product ID (Enter to cancel): ").strip().upper(),"str")
            if userInput == "":
                return 'back'
            id = inventory.search_product(userInput)
            if id != None:
                return id
    else:
        return 'back'
def update_stock():
    id = search_product()
    if id == 'back':
        return
    print("Update Stock")
    while True:
        newStock = get_valid_input(input("New Stock Quantity: "),"int")
        if newStock != "error":
            inventory.update_inventory_stock(id,newStock)
            print("\nStock updated successfully!\n")
            return

print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
file = FileSystem()
inventory = Inventory(file.load_inventory())
print("----------- MENU -----------")
print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
print("----------------------------\n")
menu()