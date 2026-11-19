import os
import unittest
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, self.supplier, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.calculate_shipping_cost(), 8.0)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, self.supplier, download_size=500)
        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)

    def test_product_type_is_not_case_sensitive(self) -> None:
        product = ProductFactory.create(" Physical ", "P001", "Desk Lamp", 25.00, 10, self.supplier)
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_value_error_with_clear_message(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_program_creates_products_through_factory(self) -> None:
        # The menu and the file system should not build products directly any more
        for filename in ["inventory_manager_oop.py", "file_system.py"]:
            with open(os.path.join(PROJECT_DIR, filename), encoding="utf-8") as file:
                source = file.read()
            self.assertNotIn("PhysicalProduct(", source, filename)
            self.assertNotIn("DigitalProduct(", source, filename)
            self.assertIn("ProductFactory.create(", source, filename)


if __name__ == "__main__":
    unittest.main()
