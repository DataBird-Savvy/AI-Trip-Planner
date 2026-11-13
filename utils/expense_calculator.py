
import sys

from exception import AITripPlannerException
class ExpenseCalculator:

    @staticmethod
    def multiply(a,b):
        """Multiply two numbers"""
        try:
            return a * b
        except Exception as e:
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

    @staticmethod
    def calculate_total(*x: float) -> float:
        """Calculate the total of a list of expenses."""
        try:
            return sum(x)
        except Exception as e:
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

    @staticmethod
    def calculate_dailybudget(total_budget: float, days: int) -> float:
        """Calculate the daily budget based on total budget and number of days."""

        if days <= 0:
            raise ValueError("Number of days must be greater than zero.")
        try:
            return total_budget / days if days > 0 else 0.0
        except Exception as e:
            raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

    