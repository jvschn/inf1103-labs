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
    def display_information_nice(self):
        print(f"ID: P00{self.__product_id}\nName: {self.__name}\nPrice: ${self.__price:.2f}\nStock: {self.__stock}")
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
                print("\nProduct Found:")
                print("------------------------------------------------")
                self.__inventory[i].display_information_nice()
                print("------------------------------------------------\n")
                return i
        print("\nProduct not found.\n")
        return 'error'
    def display_all(self):
        print("\nCurrent Inventory\n------------------------------------------------")
        if len(self.__inventory) == 0:
            print("No products found")
        else:
            for i in len(self.__inventory):
                self.__inventory[i].display_information()
        print("------------------------------------------------\n")
    def get_inventory(self):
        return self.__inventory
    def update_inventory_stock(self,id,quantity):
        self.__inventory[id].update_stock(quantity)

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

def exit_programme(inventory):
    print("\nSaving inventory before exit...")
    save_inventory(inventory)
    print("Inventory saved successfully.\n")
    generate_report(inventory)
    print("Thank you for using Inventory Management System.\nProgram terminated.")
    return

def generate_report(inventory):
    global error
    information = inventory_information(inventory)
    print("---------------------GENERATING PROCESS REPORT---------------------")
    print(f"Total Unique Products: {information[0]}")
    print(f"Total Stock Quantity: {information[1]}")
    print(f"Total Inventory Amount: ${information[2]:.2f}")
    print(f"Rejected Entries: {error}\n")

def menu():
    while True:
        userInput = get_valid_input(input("Enter option: "),"menu")
        if userInput == 1:
            inventory.display_all()
        elif userInput == 2:
            add_product()
            print("Product added successfully!\n")
        elif userInput == 3:
            newInventory = update_stock(inventory)
            if isinstance(newInventory,str) and newInventory =="back":
                continue
            else:
                inventory[newInventory[0]][1] = newInventory[1]
        elif userInput == 4:
            search = search_product(inventory)
            if isinstance(search,str) and search =="back":
                continue
        elif userInput == 5:
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json\n")
        elif userInput == 6:
            exit_programme(inventory)
            return
        else:
            print("\nError Detected...\nPlease try again.\nPlease only input nmbers 1-6.\n")
            error += 1

def add_product():
    newID = f"P{int(len(inventory.get_inventory())+1):0{3}d}"
    print("\nAdd New Product")
    print(f"Product ID: {newID}")
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
    inventory.add_product(Product(newID,nameInput,quantityInput,costInput))
    return

def update_stock():
    n=1
    print("\nUpdate Stock")
    while n<=2:
        if n==1:
            userInput = get_valid_input(input("Enter Product ID: "),"str")
            id = inventory.search_product(userInput)
            if id != 'error':
                n +=1
        elif n == 2:
            newStock = get_valid_input(input("New Stock Quantity: "),"int")
            if newStock != "error":
                inventory.update_inventory_stock(id,newStock)
                print("\nStock updated successfully!\n")
                return

print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
global inventory,file
file = FileSystem()
inventory = Inventory(file.load_inventory())
print("----------- MENU -----------")
print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
print("----------------------------\n")
menu()