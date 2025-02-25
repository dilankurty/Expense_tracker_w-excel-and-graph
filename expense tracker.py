from typing import List
from expenses import Expense
import calendar
import datetime

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000
    # Get user input for expense.
    expense = get_user_expense()
    
    # Write the expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Read the file and summarize the expenses.
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    print(f"Getting User Expense...")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    print(f"You've entered: {expense_name}, {expense_amount}")

    expense_category = [
        "Food", 
        "Utilities", 
        "Entertainment", 
        "School", 
        "Health/Insurance", 
        "Miscellaneous",
    ]

    while True:
        print("Select a category for your expense:")
        for i, category in enumerate(expense_category):
            print(f"{i+1}. {category}")
        
        value_range = f"[1 - {len(expense_category)}]"
        selected_index = int(input(f"Enter the number of the category {value_range}: ")) - 1
        if selected_index in range(len(expense_category)):
            print(f"You've selected: {expense_category[selected_index]}")
            selected_category = expense_category[selected_index]
            new_expense = Expense(name = expense_name, category = selected_category, amount = expense_amount)
            return new_expense
        
        else:
            print("Invalid category selection. Please try again.")

        break

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}...")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expense...")
    expenses: List[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expenses = Expense(
                name = expense_name, amount = float(expense_amount), category = expense_category,
                )
            expenses.append(line_expenses)
    print(expenses)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses by Category:")
    for key, amount in amount_by_category.items():
        print(f" {key}: ₱{amount:.2f}")

    total_expense = sum([ex.amount for ex in expenses])
    print(f"Total Expense: ₱{total_expense:.2f}")

    remaining_budget = budget - total_expense
    print(f"Remaining Budget: ₱{remaining_budget:.2f}")

    today = datetime.date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    remaining_days = days_in_month - today.day
    daily_budget = remaining_budget / remaining_days
    print(green(f"It's recommended to spend a daily budget of ₱{daily_budget:.2f} in the remaining days"))

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == '__main__':
    main()
