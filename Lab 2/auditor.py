inventory = 0
error = 0
entries = 0
while True:
    uinput = input("Enter the number of items in inventory: ")
    if uinput == "quit":
        print("Total Units Processed:", inventory)
        print("Total Entries Processed:", entries)
        print("Rejected Entries:", error)
        break
    if uinput.isdigit():
        if int(uinput) < 0:
            error += 1
            print("Invalid input. Please enter a non-negative number.")
        else:
            inventory += int(uinput)
            entries += 1
            print("Current inventory:", inventory)
            if inventory > 500:
                print("Warning: Inventory level is high!")
                break
    else:
        error += 1
        print("Invalid input. Please enter a number or 'quit' to exit.")