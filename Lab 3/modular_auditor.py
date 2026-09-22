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
        if int(uinput) < 0:
            error += 1
            print("Invalid input. Please enter a non-negative number.")
            return 'error'
        else:
            return user_input
    else:
        error += 1
        print("Invalid input. Please enter a number or 'quit' to exit.")
        return 'error'

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount*tax

def generate_report(total_units,total_delivered,amount_processed, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", total_delivered)
    print("Total Money Processed:", amount_processed)
    print("Rejected Entries:", failed_attempts)


while True:
    uinput = get_valid_input(input("Enter the number of items in inventory: "))
    if uinput == 'error':
        continue
    elif uinput == "quit":
        generate_report(inventory,deliveries,totalAmount,error)
        break
    else:
        if inventory + uinput > 500:
            uinput = 500-inventory
            print("Warning: Inventory only has a max of 500 units, maximum unit processed:",uinput,'\n')
        newcost = uinput*cost
        newtax = calculate_tax(newcost)
        totalcostWithTax = newcost + newtax
        totalAmount = process_delivery(totalAmount,totalcostWithTax)
        print("------------New Delivery------------\n")
        print("Number of units:",uinput)
        print("Unit cost before tax:",newcost)
        print("Delivery Tax(10%):",newtax)
        print("Total:",totalcostWithTax,'\n')
        inventory += int(uinput)
        deliveries += 1
        print("Current inventory:", inventory)
        if inventory == 500:
            break

