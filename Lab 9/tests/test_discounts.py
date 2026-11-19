import inspect
import unittest
from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount


class HalfPriceDiscount(DiscountStrategy):
    # A new strategy that only exists in this test file, Order does not know about it
    def apply(self, total: float) -> float:
        return total / 2
    def get_description(self) -> str:
        return "Half price"


class TestDiscountStrategies(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "TechSupply Pte Ltd", "sales@techsupply.com")
        self.chair = ProductFactory.create("physical", "P001", "Chair", 125.00, 10, supplier, weight=5.0)
        self.order = Order("O001")
        self.order.add_order_line(self.chair, 2)  # 2 x 125 = 250

    def test_default_is_no_discount(self) -> None:
        self.assertIsInstance(self.order.get_discount(), NoDiscount)
        self.assertEqual(self.order.calculate_total(), 250.0)

    def test_bulk_discount_over_threshold(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230.0)

    def test_bulk_discount_under_threshold(self) -> None:
        order = Order("O002", BulkDiscount(200, 20))
        order.add_order_line(self.chair, 1)  # 125 is under 200
        self.assertEqual(order.calculate_total(), 125.0)

    def test_percentage_discount(self) -> None:
        order = Order("O002", PercentageDiscount(10))
        order.add_order_line(self.chair, 2)
        self.assertEqual(order.calculate_total(), 225.0)

    def test_student_discount(self) -> None:
        self.order.set_discount(StudentDiscount())
        self.assertEqual(self.order.calculate_total(), 237.5)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230.0)
        self.order.set_discount(PercentageDiscount(10))
        self.assertEqual(self.order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        self.order.set_discount(HalfPriceDiscount())
        self.assertEqual(self.order.calculate_total(), 125.0)

    def test_same_strategy_can_be_shared_by_two_orders(self) -> None:
        discount = PercentageDiscount(10)
        order_a = Order("A", discount)
        order_b = Order("B", discount)
        self.assertIs(order_a.get_discount(), order_b.get_discount())

    def test_order_has_no_discount_if_elif_logic(self) -> None:
        source = inspect.getsource(Order)
        self.assertNotIn("elif", source)
        self.assertNotIn("discount_type", source)
        self.assertNotIn("isinstance", source)

    def test_invalid_percentage_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PercentageDiscount(0)
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


if __name__ == "__main__":
    unittest.main()
