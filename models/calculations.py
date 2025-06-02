import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

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
    balance = current_balance
    current_datetime = datetime.strptime(current_date, "%Y-%m-%d")
    target_datetime = datetime.strptime(target_date, "%Y-%m-%d")

    # Income
    for income in recurring_income_list:
        startdatetime = datetime.strptime(income[3], "%Y-%m-%d")
        frequency = income[2]
        while startdatetime <= current_datetime:
            if frequency == "weekly":
                startdatetime += timedelta(weeks=1)
            elif frequency == "biweekly":
                startdatetime += timedelta(weeks=2)
            elif frequency == "monthly":    
                startdatetime += relativedelta(months=1)
        triggers = 0
        if startdatetime < target_datetime:
            while startdatetime <= target_datetime:
                triggers += 1
                if frequency == "weekly":
                    startdatetime += timedelta(weeks=1)
                elif frequency == "biweekly":
                    startdatetime += timedelta(weeks=2)
                elif frequency == "monthly":    
                    startdatetime += relativedelta(months=1)
        balance += income[1] * triggers

    # Expenses
    for expense in recurring_expenses_list:
        startdatetime = datetime.strptime(expense[3], "%Y-%m-%d")
        frequency = expense[2]
        while startdatetime <= current_datetime:
            if frequency == "weekly":
                startdatetime += timedelta(weeks=1)
            elif frequency == "biweekly":
                startdatetime += timedelta(weeks=2)
            elif frequency == "monthly":    
                startdatetime += relativedelta(months=1)
        triggers = 0
        if startdatetime < target_datetime:
            while startdatetime <= target_datetime:
                triggers += 1
                if frequency == "weekly":
                    startdatetime += timedelta(weeks=1)
                elif frequency == "biweekly":
                    startdatetime += timedelta(weeks=2)
                elif frequency == "monthly":    
                    startdatetime += relativedelta(months=1)
        balance -= expense[1] * triggers
    return balance
    
        

