inventory = 0
cost = 1.99
tax = 0.1
error = 0
deliveries = 0
totalAmount = 0

def get_valid_input(user_input):
    if user_input == "quit":
        return user_input
    elif user_input.isdigit():
        if int(user_input) < 0:
            print("Invalid input. Please enter a non-negative number.")
            return 'error'
        else:
            return int(user_input)
    else:
        print("Invalid input. Please enter a number or 'quit' to exit.")
        return 'error'

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount*tax

def generate_report(total_units,total_delivered,amount_processed, failed_attempts):
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {total_delivered}")
    print(f"Total Money Processed: ${amount_processed:.2f}")
    print(f"Rejected Entries: {failed_attempts}")


while True:
    uinput = get_valid_input(input("Enter the number of items in inventory: "))
    if uinput == 'error':
        error += 1
        continue
    elif uinput == "quit":
        generate_report(inventory,deliveries,totalAmount,error)
        break
    else:
        if inventory + uinput > 500:
            uinput = 500-inventory
            print(f"Warning: Inventory only has a max of 500 units, maximum unit processed: {uinput}\n")
        newcost = uinput*cost
        newtax = calculate_tax(newcost)
        totalcostWithTax = newcost + newtax
        totalAmount = process_delivery(totalAmount,totalcostWithTax)
        print("------------New Delivery------------\n")
        print(f"Number of units: {uinput}")
        print(f"Unit cost before tax: ${newcost:.2f}")
        print(f"Delivery Tax(10%): ${newtax:.2f}")
        print(f"Total: ${totalcostWithTax:.2f}\n")
        inventory += int(uinput)
        deliveries += 1
        print(f"Current inventory: {inventory}\n")
        if inventory == 500:
            break
