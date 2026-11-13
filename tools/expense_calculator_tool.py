import sys

from utils.expense_calculator import ExpenseCalculator
from typing import List
from langchain.tools import tool
from logger import logger
from exception import AITripPlannerException

class CalculatorTool:
    def __init__(self):
        self.calculator = ExpenseCalculator()
        self.calculator_tool_list = self._setup_tools()
        

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night:float, total_days:float) -> float:
            """Calculate total hotel cost"""
            try:
                result = self.calculator.multiply(price_per_night, total_days)
                logger.info("Total hotel cost calculated: {}".format(result))
                print(f"Total hotel cost calculated: {result}")
                return result
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

        @tool
        def calculate_total_expense(*costs: float) -> float:
            """Calculate total expense of the trip"""
            try:
                result = self.calculator.calculate_total(*costs)
                logger.info("Total expense calculated: {}".format(result))
                print(f"Total expense calculated: {result}")
                return result
            
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            try:
                result = self.calculator.calculate_dailybudget(total_cost, days)
                logger.info("Daily expense budget calculated: {}".format(result))
                print(f"Daily expense budget calculated: {result}")
                return result
            except Exception as e:
                raise AITripPlannerException(error_message=e, error_detail=sys.exc_info())
        logger.info("Calculator tool setup complete with tools: estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget" )
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]