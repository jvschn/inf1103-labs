import unittest
from supplier import Supplier
from product_factory import ProductFactory
from order_line import OrderLine
from inventory import Inventory


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
        self.product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier)

    def test_price_zero_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Lamp", 0, 10, self.supplier)

    def test_negative_price_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", -5, 10, self.supplier)

    def test_negative_stock_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Lamp", 10, -1, self.supplier)

    def test_zero_stock_allowed(self) -> None:
        product = ProductFactory.create("physical", "P002", "Lamp", 10, 0, self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_negative_rejected_for_both_product_types(self) -> None:
        digital = ProductFactory.create("digital", "D001", "Editor", 49.90, 10, self.supplier)
        for product in [self.product, digital]:
            with self.assertRaises(ValueError):
                product.update_stock(-5)
            self.assertEqual(product.get_stock(), 10)

    def test_order_line_quantity_zero_rejected(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)

    def test_order_line_negative_quantity_rejected(self) -> None:
        with self.assertRaises(ValueError):
            OrderLine(self.product, -2)

    def test_duplicate_product_id_rejected(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.product)
        duplicate = ProductFactory.create("digital", "P001", "Other", 5.00, 1, self.supplier)
        with self.assertRaises(ValueError):
            inventory.add_product(duplicate)
        self.assertEqual(inventory.get_current_number_of_products(), 1)


if __name__ == "__main__":
    unittest.main()
