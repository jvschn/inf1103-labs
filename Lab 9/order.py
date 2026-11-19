from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount
class Order():
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        # Association: the Order uses a DiscountStrategy but does not own it
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()
    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount
    def get_discount(self) -> DiscountStrategy:
        return self.__discount
    def get_order_id(self) -> str:
        return self.__order_id
    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: the Order creates its own OrderLine objects internally.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)
    def remove_order_line(self, product_id: str) -> None:
        for order_line in self.__order_lines:
            if order_line.get_product().get_id() == product_id:
                self.__order_lines.remove(order_line)
                return
    def get_order_lines(self) -> list[OrderLine]:
        # Returns a copy so outside code cannot add, remove or move lines in this Order.
        return list(self.__order_lines)
    def get_number_of_lines(self) -> int:
        return len(self.__order_lines)
    def calculate_subtotal(self) -> float:
        return sum((order_line.calculate_subtotal() for order_line in self.__order_lines), 0.0)
    def calculate_total(self) -> float:
        total = self.calculate_subtotal()
        return self.__discount.apply(total)
    def display_information(self) -> None:
        print(f"\nOrder ID: {self.__order_id}")
        print("------------------------------------------------")
        if len(self.__order_lines) == 0:
            print("No items in this order")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("------------------------------------------------")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {self.__discount.get_description()}")
        print(f"Total: ${self.calculate_total():.2f}\n")
