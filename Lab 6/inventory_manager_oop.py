import json

class Product():
    def __init__(self, id, name, price, stock):
        self.__product_id = id
        self.__name = name
        self.__price = price
        self.__stock = 0
    def update_stock(self, quantity):
        self.__stock = quantity
    def display_information(self):
        print(f"ID: P00{self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")
    def get_id(self):
        return self.__product_id

class Inventory():
    def __init__(self,inventory):
        self.__inventory = inventory
    def add_product(self,product):
        self.__inventory.append(product)
    def search_product(self,searchid):
        for i in len(self.__inventory):
            if searchid == self.__inventory[i].get_id():
                self.__inventory[i].display_information()
                break
    def display_all(self):
        print("\nCurrent Inventory\n------------------------------------------------")
        if len(self.__inventory) == 0:
            print("No products found")
        else:
            for i in len(self.__inventory):
                self.__inventory[i].display_information()
        print("------------------------------------------------\n")

class FileSystem():
    def __init__(self):
        self.__filename = 'inventory.json'
    def save_inventory(self,inventory):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(inventory, file)
    def load_inventory(self):
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print("inventory.json found.")
            print("Inventory loaded successfully.\n")
            return data
        except:
            print("inventory.json not found.")
            data = []
            with open(self.__filename, 'w', encoding='utf-8') as file:
                json.dump(data, file)
            print("inventory.json created.")
            print("Created Inventory successfully.\n")
            return []

def get_valid_input(user_input,sequence):
    if user_input == "back":
        return user_input
    elif sequence == "menu":
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
                print("Invalid input. Please enter a postive number.\n")
                return 'error'
            else:
                return int(user_input)
        except: 
            print("Invalid input. Please input whole number.\n")
            return 'error'
    elif sequence == "price":
         try:
             if float(user_input) <= 0:
                 print("Invalid input. Please enter a postive number.\n")
                 return 'error'
             else:
                 return float(user_input)
         except: 
             print("Invalid input. Please input a number.\n")
             return 'error'

def main():
    print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
    file = FileSystem()
    inventory = Inventory(file.load_inventory())
    numOfID = len(inventory)-1
    print("----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
    print("Input \"back\" to go back to previous input in sub menus")
    print("----------------------------\n")
    menu(inventory,numOfID)