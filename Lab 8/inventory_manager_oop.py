from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from file_system import FileSystem
from inventory import Inventory
from supplier import Supplier
from product import Product
from order import Order

MENU_OPTIONS = 9

def get_valid_input(user_input: str, sequence: str) -> int | float | str | None:
    if sequence == "menu":
        try:
            if int(user_input)<1 or int(user_input)>MENU_OPTIONS:
                print(f"\nPlease only input numbers 1-{MENU_OPTIONS}.\n")
            else:
                return int(user_input)
        except:
            print(f"\nPlease only input numbers 1-{MENU_OPTIONS}.\n")
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

def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Shipping information\n7. Remove Product\n8. Create Order\n9. Exit")
    print("----------------------------\n")

def exit_programme() -> None:
    print("\nSaving inventory before exit...")
    file.save_inventory(inventory.get_inventory())
    print("Inventory saved successfully.\n")
    print("Thank you for using Inventory Management System.\nProgram terminated.")
    return


def menu() -> None:
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
            remove_product()
        elif userInput == 8:
            create_order()
        elif userInput == 9:
            exit_programme()
            return
        else:
            continue
def shipping_information() -> None:
    if inventory.print_product_ids():
        userInput = get_valid_input(input("Enter Product ID (Enter to cancel): ").strip().upper(),"str")
        if userInput == "":
            return
        inventory.shipping_information(userInput)
def get_supplier() -> Supplier:
    print("Supplier Details")
    while True:
        supplierID = get_valid_input(input("Supplier ID: ").strip().upper(),"str")
        if supplierID != "":
            break
        print("Supplier ID cannot be empty.\n")
    while True:
        supplierName = get_valid_input(input("Supplier Name: ").strip(),"str")
        if supplierName != "":
            break
        print("Supplier Name cannot be empty.\n")
    while True:
        supplierEmail = get_valid_input(input("Supplier Email: ").strip(),"str")
        if "@" in supplierEmail:
            break
        print("Please enter a valid email address.\n")
    return Supplier(supplierID,supplierName,supplierEmail)
def add_product() -> None:
    newID = inventory.generate_next_id()
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
    supplier = get_supplier()
    while True:
        print("Choose a product type:\n1: Physical\n2: Digital")
        typeInput = get_valid_input(input("Type: "),"int")
        if typeInput == 1:
            weightInput = get_valid_input(input("Weight(kg): "),"float")
            if weightInput != "error":
                inventory.add_product(PhysicalProduct(newID,nameInput,costInput,quantityInput,weightInput,supplier))
                break
        elif typeInput == 2:
            download_sizeInput = get_valid_input(input("Download Size(mb): "),"float")
            if download_sizeInput != "error":
                inventory.add_product(DigitalProduct(newID,nameInput,costInput,quantityInput,download_sizeInput,supplier))
                break
        else:
            print("Please only input 1 or 2\n")
    return
def search_product() -> Product | None:
    if inventory.print_product_ids():
        while True:
            userInput = get_valid_input(input("Enter Product ID (Enter to cancel): ").strip().upper(),"str")
            if userInput == "":
                return None
            product = inventory.search_product(userInput)
            if product is not None:
                return product
    return None
def update_stock() -> None:
    product = search_product()
    if product is None:
        return
    print("Update Stock")
    while True:
        newStock = get_valid_input(input("New Stock Quantity: "),"int")
        if newStock != "error":
            inventory.update_inventory_stock(product.get_id(),newStock)
            print("\nStock updated successfully!\n")
            return
def remove_product() -> None:
    product = search_product()
    if product is None:
        return
    confirm = input(f"Remove {product.get_id()} from the inventory? (Y/N): ").strip().upper()
    if confirm == "Y":
        inventory.remove_product(product.get_id())
        print(f"\n{product.get_id()} removed from the inventory.\n")
    else:
        print("\nRemoval cancelled.\n")
def create_order() -> None:
    global order_count
    if not inventory.print_product_ids():
        return
    order_count += 1
    order = Order(f"O{order_count:03d}")
    print(f"Creating Order {order.get_order_id()}")
    while True:
        productID = input("Enter Product ID to add (Enter to finish): ").strip().upper()
        if productID == "":
            break
        product = inventory.find_product(productID)
        if product is None:
            print("Product not found.\n")
            continue
        quantity = get_valid_input(input("Quantity: "),"int")
        if quantity == "error":
            continue
        order.add_order_line(product,quantity)
        print(f"Added {quantity} x {product.get_name()} to the order.\n")
    if order.get_number_of_lines() == 0:
        print("\nNo items added. Order cancelled.\n")
        return
    order.display_information()

print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
file = FileSystem()
inventory = Inventory(file.load_inventory())
order_count = 0
print_menu()
menu()
