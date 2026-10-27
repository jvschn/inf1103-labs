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
    def __init__(self):
        self.__inventory = []
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
