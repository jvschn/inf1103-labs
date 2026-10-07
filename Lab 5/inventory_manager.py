import json
global error,tax
tax = 0.1
error = 0

# #Name, Stock, Price
# inventory = {
#     "Total":0,
#     "P001": ["Laptop",15,1200],
#     "P002": ["Mouse",40,25.5],
#     "P003": ["Keyboard",25,45],
# }
def calculate_tax(amount):
    global tax
    return float("{:.2f}".format(amount*tax))

def save_inventory(inventory):
    with open('inventory.json', 'w', encoding='utf-8') as file:
        json.dump(inventory, file)

def load_inventory():
    try:
        with open('inventory.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print("inventory.json found.")
        print("Inventory loaded successfully.\n")
        return data
    except:
        print("inventory.json not found.")
        data = {'Information':{}}
        with open('inventory.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)
        print("inventory.json created.")
        print("Created Inventory successfully.\n")
        return data



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


def menu(inventory,numOfID):
    global error
    while True:
        userInput = get_valid_input(input("Enter option: "),"menu")
        if userInput == 1:
            display_all(inventory,numOfID)
        elif userInput == 2:
            newProduct = add_product(numOfID+1)
            if isinstance(newProduct,str) and newProduct =="back":
                continue
            else: 
                numOfID += 1
                inventory[f"P{int(numOfID):0{3}d}"] = newProduct
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

def main():
    print("========================================\nINVENTORY MANAGEMENT SYSTEM\n========================================\n")
    inventory = load_inventory()
    numOfID = len(inventory)-1
    print("----------- MENU -----------")
    print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
    print("Input \"back\" to go back to previous input in sub menus")
    print("----------------------------\n")
    menu(inventory,numOfID)


def display_all(inventory,ID):
    print("\nCurrent Inventory\n------------------------------------------------")
    if ID == 0:
        print("No products found")
    else:
        for i in range(ID):
            current = inventory[f"P{int(i+1):0{3}d}"]
            print(f"ID: P00{i+1} | Name: {current[0]} | Price: ${current[2]:.2f} | Stock: {current[1]}")
    print("------------------------------------------------\n")

def add_product(ID):
    global error
    n=1
    print("\nAdd New Product")
    print(f"Product ID: P{int(ID):0{3}d}")
    while n < 4:
        if n == 1:
            nameInput = get_valid_input(input("Product Name: "),"str")
            if nameInput == "back":
                print("Returning to Menu...\n")
                return nameInput
            elif nameInput == "error":
                error +=1
            else: 
                n += 1
        elif n ==2:
            costInput = get_valid_input(input("Price: $"),"price")
            if costInput == "back":
                n-=1
            elif costInput == "error":
                error +=1
            else:
                costInput = float("{:.2f}".format(costInput))
                n += 1
        else:
            quantityInput = get_valid_input(input("Stock Quantity: "),"int")
            if quantityInput == "back":
                n -=1
            elif quantityInput == "error":
                error +=1
            else: 
                n += 1
                break
    return[nameInput,quantityInput,costInput]

def update_stock(inventory):
    global error
    n=1
    print("\nUpdate Stock")
    while n<=2:
        if n==1:
            userInput = get_valid_input(input("Enter Product ID: "),"str")
            if userInput == "back":
                print("Returning to Menu...\n")
                return userInput
            else:
                try:
                    product = inventory[userInput]
                    print("\nProduct Found:")
                    print(f"Name: {product[0]}")
                    print(f"Current Stock: {product[1]}\n")
                    n+=1
                except:
                    print("\nProduct not found.\n")
        elif n == 2:
            newStock = get_valid_input(input("New Stock Quantity: "),"int")
            if newStock == "back":
                n -=1
            elif newStock == "error":
                error +=1
            else:
                print("\nStock updated successfully!\n")
                n+=1
                return [userInput,newStock]

def search_product(inventory):
    print("\nSearch Stock")
    while True:
        userInput = get_valid_input(input("Enter Product ID: "),"str")
        if userInput == "back":
            print("Returning to Menu...\n")
            return userInput
        else:
            try:
                product = inventory[userInput]
                print("\nProduct Found:")
                print("------------------------------------------------")
                print(f"Name: {product[0]}")
                print(f"Price: ${product[2]:.2f}")
                print(f"Current Stock: {product[1]}")
                print("------------------------------------------------\n")
                return
            except:
                print("\nProduct not found.\n")

def exit_programme(inventory):
    print("\nSaving inventory before exit...")
    save_inventory(inventory)
    print("Inventory saved successfully.\n")
    generate_report(inventory)
    print("Thank you for using Inventory Management System.\nProgram terminated.")
    return

def inventory_information(inventory):
    products = len(inventory)-1
    totalStock = 0
    totalAmount = 0
    for i in range(products):
        current = inventory[f"P{int(i+1):0{3}d}"]
        price = current[2]
        totalStock += current[1]
        totalAmount += current[1]*price
    return [products,totalStock,totalAmount]  

def generate_report(inventory):
    global error
    information = inventory_information(inventory)
    print("---------------------GENERATING PROCESS REPORT---------------------")
    print(f"Total Unique Products: {information[0]}")
    print(f"Total Stock Quantity: {information[1]}")
    print(f"Total Inventory Amount: ${information[2]:.2f}")
    print(f"Rejected Entries: {error}\n")


main()















