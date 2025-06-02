import json
from datetime import datetime

# Constants
current_balance = 0.0
current_date = datetime.now().strftime("%Y-%m-%d")
target_date = None
recurring_income_list = []
recurring_expenses_list = []

def set_constants():
    try:
        with open("data/financial_data.json", "r") as file:
            data = json.load(file)
            global current_balance, target_date, recurring_income, recurring_expenses
            current_balance = data.get("current_balance", 0.0)
            target_date = data.get("target_date", None)
            recurring_income_list = [
                    (item["name"], item["amount"], item["frequency"], item["start_date"])
                    for item in data.get("recurring_income", [])
                ]
            recurring_expenses_list = [
                    (item["name"], item["amount"], item["frequency"], item["start_date"])
                    for item in data.get("recurring_expenses", [])
                ]
    except FileNotFoundError:
        print("Financial data file not found. Using default values.")
    except json.JSONDecodeError:
        print("Error decoding financial data.")
    except Exception as e:
        print(f"Error loading data: {e}")

    print(f"Current Balance: {current_balance}")
    print(f"Current Date: {current_date}")
    print(f"Target Date: {target_date}")
    print(f"Recurring Income: {recurring_income_list}")
    print(f"Recurring Expenses: {recurring_expenses_list}")

def calculate_future_balance():
    global current_balance
    for income in recurring_income_list:
        number_triggers = 0
        if target_date > current_date:
            start_date = datetime.strptime(income[3], "%Y-%m-%d")
            end_date = datetime.strptime(target_date, "%Y-%m-%d")
            if income[2] == "monthly":
                number_triggers = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            elif income[2] == "weekly":
                number_triggers = (end_date - start_date).days // 7
            elif income[2] == "daily":
                number_triggers = (end_date - start_date).days
            
            current_balance += income[1] * number_triggers

    for expense in recurring_expenses_list:
        number_triggers = 0
        if target_date > current_date:
            start_date = datetime.strptime(expense[3], "%Y-%m-%d")
            end_date = datetime.strptime(target_date, "%Y-%m-%d")
            if expense[2] == "monthly":
                number_triggers = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            elif expense[2] == "weekly":
                number_triggers = (end_date - start_date).days // 7
            elif expense[2] == "daily":
                number_triggers = (end_date - start_date).days
            
            current_balance -= expense[1] * number_triggers
    return current_balance

