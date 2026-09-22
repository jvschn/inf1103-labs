inventory = 0
cost = 1.99
tax = 0.1
error = 0
entries = 0
totalAmount = 0

def get_valid_input(user_input):
    if user_input == "quit":
        return user_input
    elif user_input.isdigit():
        if int(uinput) < 0:
            error += 1
            print("Invalid input. Please enter a non-negative number.")
        else:
            return
    else:
        error += 1
        print("Invalid input. Please enter a number or 'quit' to exit.")

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount*tax

def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", inventory)
    print("Total Deliveries Processed:", entries)
    print("Total Money Processed:", totalAmount)
    print("Rejected Entries:", error)

while True:
    uinput = input("Enter the number of items in inventory: ")
    if uinput == "quit":
        print("Total Units Processed:", inventory)
        print("Total Deliveries Processed:", entries)
        print("Total Money Processed:", totalAmount)
        print("Rejected Entries:", error)
        break
    if uinput.isdigit():
        if int(uinput) < 0:
            error += 1
            print("Invalid input. Please enter a non-negative number.")
        else:
            inventory += int(uinput)
            if inventory > 500:
                inventory = 500
                print("Current inventory:", inventory)
                print("Warning: Inventory level is high!")
                break
            entries += 1
            print("Current inventory:", inventory)
    else:
        error += 1
        print("Invalid input. Please enter a number or 'quit' to exit.")

