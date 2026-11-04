class ExpenseCalculator:

    @staticmethod
    def multiply(a,b):
        """Multiply two numbers"""
        return a * b

    @staticmethod
    def calculate_total(*x: float) -> float:
        """Calculate the total of a list of expenses."""

        return sum(x)

    @staticmethod
    def calculate_dailybudget(total_budget: float, days: int) -> float:
        """Calculate the daily budget based on total budget and number of days."""

        if days <= 0:
            raise ValueError("Number of days must be greater than zero.")
        return total_budget / days if days > 0 else 0.0

    