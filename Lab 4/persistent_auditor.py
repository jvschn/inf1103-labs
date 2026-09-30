import csv
import ast
global error
tax = 0.1
error = 0

def load_inventory():
    try:
        with open('inventory.txt', mode='r', encoding='utf-8') as file:
            read_data = list(csv.DictReader(file))
        if len(read_data) == 0:
            return{'Total':0}
        else:
            data = {}
            for i in read_data[0]:
                data[i] = ast.literal_eval(read_data[0][i])
            return data
    except:
        with open("inventory.txt", mode="w", newline="") as file:
            pass
        return{'Total':0}

def save_inventory(inventory):
    with open("inventory.txt", mode="w", newline="") as file:
        write_data = csv.DictWriter(file, inventory.keys())
        write_data.writeheader()
        write_data.writerow(inventory)
    print("Orders succesfully saved to inventory.csv\n")



def get_valid_input(user_input,sequence):
    if user_input == "quit":
        return user_input
    elif user_input == "cancel":
        return user_input
    elif sequence == 1:
        return user_input
    elif sequence == 2:
        try:
            if int(user_input) <= 0:
                print("Invalid input. Please enter a postive number.\n")
                return 'error'
            else:
                return int(user_input)
        except: 
            print("Invalid input. Please input whole number.\n")
            return 'error'
    elif sequence == 3:
         try:
             if float(user_input) <= 0:
                 print("Invalid input. Please enter a postive number.\n")
                 return 'error'
             else:
                 return float(user_input)
         except: 
             print("Invalid input. Please input a number.\n")
             return 'error'       

def userPrompts():
    global error
    n=1
    print("Add new order by filling up the prompts below with the appropirate inputs.\n")
    while n < 4:
        if n == 1:
            nameInput = get_valid_input(input("Enter Product Name: "),n)
            if nameInput == "cancel":
                print("Nothing to go back to...Please input the name of your product or \"quit\" \n")
            elif nameInput == "quit":
                return nameInput
            elif nameInput == "error":
                error +=1
            else: 
                n += 1
        elif n ==2:
            quantityInput = get_valid_input(input("Enter Product Quantity: "),n)
            if quantityInput == "cancel":
                n -=1
            elif quantityInput == "quit":
                return quantityInput
            elif quantityInput == "error":
                error +=1
            else: 
                n += 1
        else:
            costInput = get_valid_input(input("Enter Product Cost(for 1 product): $"),n)
            if costInput == "cancel":
                n-=1
            elif costInput == "quit":
                return costInput
            elif costInput == "error":
                error +=1
            else:
                costInput = float("{:.2f}".format(costInput))
                n += 1
                break
    return[nameInput,quantityInput,costInput]

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return float("{:.2f}".format(amount*tax))

def generate_report(total_delivered,total_units,amount_processed, failed_attempts):
    print("---------------------GENERATING PROCESS REPORT---------------------")
    print(f"Total Orders Processed: {total_delivered}")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Money Processed: ${amount_processed:.2f}")
    print(f"Rejected Entries: {failed_attempts}")

# save_inventory(inventory)
inventory = load_inventory()
deliveries = len(inventory)-1
totalAmount = 0
totalUnits = 0

print("Welcome to the updated Inventory Auditor Program!\n")
if deliveries == 0:
    print("Currently you have no active orders.\n")
else:
    print("Current Orders:\n")
    for i in range(deliveries):
        current = inventory[str(1000+i+1)]
        print(f"{str(1000+i+1)}, {current[0]}, {current[1]}, ${current[2]:.2f}")
        totalUnits += int(current[1])
        totalAmount += float(current[2])
    print("\n")
print("To use this program, here are the lists of input commands:\n\"quit\" is used to quit the program at any time.\n\"cancel\" is used to go to the previous input.\nOther than the top 2, only valid positive numbers are allowed in the quantity and cost prompts.\n")

while True:
    if totalUnits == 500:
        save_inventory(inventory)
        print("Max number of units reached. Program will save and auto exit. Thank you!\n")
        generate_report(deliveries,totalUnits,totalAmount,error)
        break
    newOrder = userPrompts()
    if newOrder == "quit":
        save_inventory(inventory)
        generate_report(deliveries,totalUnits,totalAmount,error)
        break
    elif totalUnits + newOrder[1] > 500:
        print(f"Warning: Inventory only has a max of 500 units, maximum units that can still be processed is: {500 - totalUnits}")
        print(f"Do not input more than {500 - totalUnits} products.\n")
        error += 1
    else:
        deliveries +=1
        inventory[str(1000+deliveries)] = newOrder
        totalCost = newOrder[2]*newOrder[1]
        ordertax = calculate_tax(totalCost)
        totalcostWithTax = float("{:.2f}".format(totalCost + ordertax))
        totalAmount = process_delivery(totalAmount,totalcostWithTax)
        inventory['Total'] = float("{:.2f}".format(totalAmount))
        totalUnits += newOrder[1]
        print("------------New Order------------\n")
        print(f"Order Number: {str(1000+deliveries)}")
        print(f"Product Name: {newOrder[0]}")
        print(f"Number of Products: {newOrder[1]}")
        print(f"Unit cost before tax: ${newOrder[2]:.2f} x {newOrder[1]} = ${totalCost:.2f}")
        print(f"Delivery Tax(10%): ${ordertax:.2f}")
        print(f"Total: ${totalcostWithTax:.2f}\n")
        del inventory[str(1000+deliveries)][-1]
        inventory[str(1000+deliveries)].append(totalcostWithTax)