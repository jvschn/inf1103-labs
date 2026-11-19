import io
import os
import re
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from supplier import Supplier
from inventory import Inventory
from file_system import FileSystem
from product_loader import load_products
from input_helpers import get_positive_float, get_positive_int, get_non_negative_int

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TESTS_DIR)
PRODUCTS_CSV = os.path.join(TESTS_DIR, "products_test.csv")


class TestUserInput(unittest.TestCase):
    def test_get_positive_float_keeps_asking_until_valid(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), redirect_stdout(output):
            value = get_positive_float("Price: $")
        self.assertEqual(value, 12.5)
        lines = output.getvalue().splitlines()
        self.assertEqual(lines, ["Please enter a valid number, e.g. 12.50",
                                 "Please enter a number greater than zero."])

    def test_get_positive_int_rejects_zero_and_text(self) -> None:
        with patch("builtins.input", side_effect=["two", "0", "3"]), redirect_stdout(io.StringIO()):
            self.assertEqual(get_positive_int("Quantity: "), 3)

    def test_get_non_negative_int_allows_zero(self) -> None:
        with patch("builtins.input", side_effect=["-1", "0"]), redirect_stdout(io.StringIO()):
            self.assertEqual(get_non_negative_int("Stock: "), 0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
        self.inventory = Inventory()

    def run_load(self, path: str) -> str:
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_valid_rows_load_and_bad_rows_are_skipped(self) -> None:
        output = self.run_load(PRODUCTS_CSV)
        self.assertEqual(self.inventory.get_current_number_of_products(), 3)
        for product_id in ["P001", "D001", "P003"]:
            self.assertIsNotNone(self.inventory.find_product(product_id))
        self.assertIsNone(self.inventory.find_product("S001"))
        self.assertIsNone(self.inventory.find_product("P002"))
        self.assertIn("Unknown product type: service", output)
        self.assertIn("could not convert string to float: 'abc'", output)

    def test_messages_print_in_the_right_order(self) -> None:
        lines = self.run_load(PRODUCTS_CSV).splitlines()
        self.assertTrue(lines[0].startswith("Skipped row 4"))
        self.assertTrue(lines[1].startswith("Skipped row 5"))
        self.assertEqual(lines[2], "3 products loaded.")
        self.assertEqual(lines[3], "Load attempt finished.")

    def test_missing_file_handled_gracefully(self) -> None:
        output = self.run_load(os.path.join(TESTS_DIR, "does_not_exist.csv"))
        self.assertIn("Products file not found", output)
        self.assertNotIn("products loaded", output)  # else block did not run
        self.assertIn("Load attempt finished.", output)  # finally block did run
        self.assertEqual(self.inventory.get_current_number_of_products(), 0)


class TestFileSystem(unittest.TestCase):
    def setUp(self) -> None:
        self.old_dir = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

    def tearDown(self) -> None:
        os.chdir(self.old_dir)
        self.temp_dir.cleanup()

    def test_corrupted_json_does_not_crash(self) -> None:
        with open("inventory.json", "w", encoding="utf-8") as file:
            file.write("{this is not json")
        with redirect_stdout(io.StringIO()):
            products = FileSystem().load_inventory()
        self.assertEqual(products, [])

    def test_invalid_product_in_json_is_skipped(self) -> None:
        supplier = {"supplier_id": "S001", "name": "TechSupply", "contact_email": "a@b.com"}
        data = [
            {"type": "physical", "id": "P001", "name": "Lamp", "price": 25.0, "stock": 10, "weight": 1.0, "supplier": supplier},
            {"type": "service", "id": "S001", "name": "Install", "price": 30.0, "stock": 5, "supplier": supplier},
            {"type": "digital", "id": "D001", "name": "Editor", "price": -1, "stock": 5, "download_size": 2.0, "supplier": supplier},
            {"type": "digital", "id": "D002", "name": "Missing price", "stock": 5, "supplier": supplier},
        ]
        with open("inventory.json", "w", encoding="utf-8") as file:
            json.dump(data, file)
        with redirect_stdout(io.StringIO()):
            products = FileSystem().load_inventory()
        self.assertEqual([p.get_id() for p in products], ["P001"])


class TestSpecificExceptions(unittest.TestCase):
    def test_no_bare_except_in_project(self) -> None:
        for filename in os.listdir(PROJECT_DIR):
            if filename.endswith(".py"):
                with open(os.path.join(PROJECT_DIR, filename), encoding="utf-8") as file:
                    source = file.read()
                self.assertIsNone(re.search(r"except\s*:", source), f"bare except in {filename}")


if __name__ == "__main__":
    unittest.main()
