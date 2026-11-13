from tools.expense_calculator_tool import CalculatorTool


def test_estimate_total_hotel_cost():

    calculator = CalculatorTool()

    tool = calculator.calculator_tool_list[0]

    result = tool.invoke({
        "price_per_night": 1000,
        "total_days": 5
    })

    assert result == 5000