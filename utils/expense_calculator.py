class ExpenseCalculator:

    @staticmethod
    def multiply(a,b):
        return a * b

    @staticmethod
    def calculate(*x: float) -> float:
        return sum(x)

    @staticmethod
    def calculate_dailybudget(total_budget: float, days: int) -> float:
        if days <= 0:
            raise ValueError("Number of days must be greater than zero.")
        return total_budget / days if days > 0 else 0.0

    