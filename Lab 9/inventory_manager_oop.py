from product_factory import ProductFactory
from file_system import FileSystem
from inventory import Inventory
from supplier import Supplier
from product import Product
from order import Order
from discount_strategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from input_helpers import get_positive_float, get_positive_int, get_non_negative_int
from product_loader import load_products

MENU_OPTIONS = 10

def get_valid_input(user_input: str, sequence: str) -> int | str | None:
    if sequence == "menu":
        try:
            if int(user_input)<1 or int(user_input)>MENU_OPTIONS:
                print(f"\nPlease only input numbers 1-{MENU_OPTIONS}.\n")
            else:
                return int(user_input)
        except ValueError:
            print(f"\nPlease only input numbers 1-{MENU_OPTIONS}.\n")
    elif sequence == "str":
        return user_input
    return None

def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Shipping information\n7. Remove Product\n8. Create Order\n9. Load Products from CSV\n10. Exit")
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
            load_products_from_csv()
        elif userInput == 10:
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
    while True:
        nameInput = input("Product Name: ").strip()
        if nameInput != "":
            break
        print("Product Name cannot be empty.\n")
    costInput = round(get_positive_float("Price: $"), 2)
    quantityInput = get_non_negative_int("Stock Quantity: ")
    supplier = get_supplier()
    while True:
        print("Choose a product type:\n1: Physical\n2: Digital")
        typeInput = input("Type: ").strip()
        if typeInput == "1":
            weightInput = get_positive_float("Weight(kg): ")
            productType, weight, downloadSize = "physical", weightInput, 0.0
            break
        elif typeInput == "2":
            downloadSize = get_positive_float("Download Size(mb): ")
            productType, weight = "digital", 0.0
            break
        else:
            print("Please only input 1 or 2\n")
    try:
        product = ProductFactory.create(productType,newID,nameInput,costInput,quantityInput,supplier,weight=weight,download_size=downloadSize)
        inventory.add_product(product)
    except ValueError as e:
        print(f"\nProduct could not be added: {e}\n")
        return
    print("Product added successfully!\n")
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
    newStock = get_non_negative_int("New Stock Quantity: ")
    inventory.update_inventory_stock(product.get_id(),newStock)
    print("\nStock updated successfully!\n")
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
        quantity = get_positive_int("Quantity: ")
        order.add_order_line(product,quantity)
        print(f"Added {quantity} x {product.get_name()} to the order.\n")
    if order.get_number_of_lines() == 0:
        print("\nNo items added. Order cancelled.\n")
        return
    order.set_discount(choose_discount())
    order.display_information()
def choose_discount() -> DiscountStrategy:
    discounts: dict[str, DiscountStrategy] = {
        "1": NoDiscount(),
        "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20),
        "4": StudentDiscount(),
    }
    print("\nChoose a discount:")
    for key, discount in discounts.items():
        print(f"{key}: {discount.get_description()}")
    while True:
        choice = input("Discount: ").strip()
        if choice in discounts:
            return discounts[choice]
        print(f"Please only input 1-{len(discounts)}\n")
def load_products_from_csv() -> None:
    path = input("CSV file name (Enter for products.csv): ").strip()
    if path == "":
        path = "products.csv"
    supplier = get_supplier()
    print()
    load_products(path, inventory, supplier)
    print()

print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
file = FileSystem()
inventory = Inventory(file.load_inventory())
order_count = 0
print_menu()
menu()
