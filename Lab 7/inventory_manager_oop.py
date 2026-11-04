from product import DigitalProduct,PhysicalProduct
from file_system import FileSystem
from inventory import Inventory

def get_valid_input(user_input,sequence):
    if sequence == "menu":
        try:
            if int(user_input)<1 or int(user_input)>7:
                print("\nPlease only input numbers 1-7.\n")
            else:
                return int(user_input)
        except:
            print("\nPlease only input numbers 1-7.\n")
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
    elif sequence == "float":
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
            shipping_information()
        elif userInput == 7:
            exit_programme()
            return
        else:
            continue
def shipping_information():
    if inventory.print_product_ids() != 'error':
        while True:
            userInput = get_valid_input(input("Enter Product ID (Enter to cancel): ").strip().upper(),"str")
            if userInput == "":
                return 'back'
            inventory.shipping_information(userInput)
            return
    else:
        return
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
            costInput = get_valid_input(input("Price: $"),"float")
            if costInput != "error":
                costInput = float("{:.2f}".format(costInput))
                n += 1
        else:
            quantityInput = get_valid_input(input("Stock Quantity: "),"int")
            if quantityInput != "error":
                n += 1
                break
    while True:
        print("Choose a product type:\n1: Physical\n2: Digital")
        typeInput = get_valid_input(input("Type: "),"int")
        if typeInput == 1:
            weightInput = get_valid_input(input("Weight(kg): "),"float")
            if weightInput != "error":
                inventory.add_product(PhysicalProduct(newID,nameInput,costInput,quantityInput,weightInput))
                break
        elif typeInput == 2:
            download_sizeInput = get_valid_input(input("Download Size(mb): "),"float")
            if download_sizeInput != "error":
                inventory.add_product(DigitalProduct(newID,nameInput,costInput,quantityInput,download_sizeInput))
                break
        else:
            print("Please only input 1 or 2\n")
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
print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Shipping information\n7. Exit")
print("----------------------------\n")
menu()