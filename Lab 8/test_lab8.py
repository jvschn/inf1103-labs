from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def test_association() -> None:
    print("========== Section 2: Association (Supplier - Product) ==========\n")

    # 1. Create a Supplier object independently
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")

    # 2. Create a PhysicalProduct and a DigitalProduct using that Supplier
    physical = PhysicalProduct("P001", "Phone", 1000.00, 50, 2.3, supplier)
    digital = DigitalProduct("P002", "Windows 10", 120.20, 32, 1023.2, supplier)

    # 3. Display the supplier information through each Product
    print("Supplier through PhysicalProduct:")
    physical.get_supplier().display_information()
    print("\nSupplier through DigitalProduct:")
    digital.get_supplier().display_information()

    # 4. Confirm Supplier and Products are separate objects
    print("\n--- Separate objects check ---")
    print(f"id(supplier)                = {id(supplier)}")
    print(f"id(physical.get_supplier()) = {id(physical.get_supplier())}")
    print(f"id(digital.get_supplier())  = {id(digital.get_supplier())}")
    print(f"id(physical)                = {id(physical)}")
    print(f"id(digital)                 = {id(digital)}")
    print(f"Both products share the same Supplier object: {physical.get_supplier() is digital.get_supplier()}")
    print(f"Supplier is a different object from the products: {supplier is not physical and supplier is not digital}")

    # 5. Predict first: delete the supplier variable
    print("\n--- After 'del supplier' ---")
    del supplier
    try:
        supplier.display_information()
    except NameError as e:
        print(f"Using the deleted variable name: NameError -> {e}")

    print("\nPhysicalProduct can still display its supplier:")
    physical.get_supplier().display_information()
    print("\nDigitalProduct can still display its supplier:")
    digital.get_supplier().display_information()
    print()


def test_aggregation() -> None:
    print("========== Section 3: Aggregation (Inventory - Product) ==========\n")
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")

    # 1. Create a Product before any Inventory exists
    phone = PhysicalProduct("P001", "Phone", 1000.00, 50, 2.3, supplier)
    print("Product created before any Inventory:")
    phone.display_information()

    # 2. Add the Product to Inventory A
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(phone)
    print(f"\nAdded to Inventory A. Products in A: {inventory_a.get_current_number_of_products()}")
    print(f"find_product('P001') in A is phone: {inventory_a.find_product('P001') is phone}")

    # 3. Remove it from Inventory A and confirm the Product can still be used
    inventory_a.remove_product("P001")
    print(f"\nRemoved from Inventory A. Products in A: {inventory_a.get_current_number_of_products()}")
    print(f"find_product('P001') in A: {inventory_a.find_product('P001')}")
    print("Product still works after removal:")
    phone.update_stock(45)
    phone.display_information()
    print(phone.get_fulfilment_info())

    # 4. Add the same Product object to Inventory B
    inventory_b.add_product(phone)
    print(f"\nAdded the same object to Inventory B. Products in B: {inventory_b.get_current_number_of_products()}")
    print(f"Object in B is the same object as the original: {inventory_b.find_product('P001') is phone}")

    # 5. Empty an inventory - the Product is not destroyed
    inventory_b.remove_product("P001")
    del inventory_a, inventory_b
    print("\nBoth inventories emptied and deleted. Product still exists:")
    phone.display_information()
    print()


def test_composition() -> None:
    print("========== Section 4: Composition (Order - OrderLine) ==========\n")
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
    phone = PhysicalProduct("P001", "Phone", 1000.00, 50, 2.3, supplier)
    windows = DigitalProduct("P002", "Windows 10", 120.20, 32, 1023.2, supplier)

    # 1-3. Create an Order, add products, display lines and total
    order1 = Order("O001")
    order1.add_order_line(phone, 2)
    order1.add_order_line(windows, 3)
    order1.display_information()

    # 4. Add the same Product to a different Order
    order2 = Order("O002")
    order2.add_order_line(phone, 1)
    order2.display_information()

    line_in_order1 = order1.get_order_lines()[0]
    line_in_order2 = order2.get_order_lines()[0]
    print("--- Same Product in two Orders ---")
    print(f"id(line in O001) = {id(line_in_order1)}")
    print(f"id(line in O002) = {id(line_in_order2)}")
    print(f"Same OrderLine object?  {line_in_order1 is line_in_order2}")
    print(f"id(product in O001 line) = {id(line_in_order1.get_product())}")
    print(f"id(product in O002 line) = {id(line_in_order2.get_product())}")
    print(f"Same Product object?    {line_in_order1.get_product() is line_in_order2.get_product()}")
    print("Result: 2 OrderLine objects (one per Order), 1 Product object (shared).")

    # 5. Remove an order line through the Order, then remove the whole Order
    print("\nRemoving P002 line from O001 using order1.remove_order_line('P002'):")
    order1.remove_order_line("P002")
    order1.display_information()

    del order1
    print("Order O001 deleted - its OrderLines go with it, but the Product still exists:")
    phone.display_information()
    print()


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    print("========== Section 6: Liskov Substitution Principle ==========\n")
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
    phone = PhysicalProduct("P001", "Phone", 1000.00, 50, 2.3, supplier)
    windows = DigitalProduct("P002", "Windows 10", 120.20, 32, 1023.2, supplier)

    # 6.2 The same function works for both subclasses without changes
    print("show_product_details(PhysicalProduct):")
    show_product_details(phone)
    print("\nshow_product_details(DigitalProduct):")
    show_product_details(windows)

    # Both subclasses keep the update_stock() expectation set by Product
    print("\nupdate_stock(10) on both, then update_stock(-5) (should be ignored by both):")
    for product in [phone, windows]:
        product.update_stock(10)
        product.update_stock(-5)
        print(f"{product.get_id()} stock = {product.get_stock()}")

    # Both types used by normal Inventory operations
    inventory = Inventory()
    inventory.add_product(phone)
    inventory.add_product(windows)
    inventory.update_inventory_stock("P001", 20)
    inventory.update_inventory_stock("P002", 30)
    inventory.display_all()


def test_polymorphism() -> None:
    print("========== Section 7: Polymorphism ==========\n")
    supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Phone", 1000.00, 50, 2.3, supplier))
    inventory.add_product(DigitalProduct("P002", "Windows 10", 120.20, 32, 1023.2, supplier))

    # One loop, no isinstance() - each object runs its own implementation
    for product in inventory.get_inventory():
        print(f"[{type(product).__name__}]")
        product.display_information()
        print(product.get_fulfilment_info())
        print()


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
