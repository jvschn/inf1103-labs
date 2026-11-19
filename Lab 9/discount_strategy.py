from abc import ABC, abstractmethod
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass
    @abstractmethod
    def get_description(self) -> str:
        pass
class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total
    def get_description(self) -> str:
        return "No discount"
class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage
    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)
    def get_description(self) -> str:
        return f"{self.__percentage:g}% off"
class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        if threshold <= 0 or amount <= 0:
            raise ValueError("Threshold and amount must be greater than zero.")
        self.__threshold: float = threshold
        self.__amount: float = amount
    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return round(total - self.__amount, 2)
        return total
    def get_description(self) -> str:
        return f"${self.__amount:.2f} off orders of ${self.__threshold:.2f} or more"
class StudentDiscount(DiscountStrategy):
    # Added after Order was finished, Order did not need to change
    def apply(self, total: float) -> float:
        return round(total * 0.95, 2)
    def get_description(self) -> str:
        return "Student discount (5% off)"
