import csv
from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory
def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name, float(price), int(stock_quantity), supplier)
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipped row {row_number} {row}: {e}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
