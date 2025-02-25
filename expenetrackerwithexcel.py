from typing import List
from expenses import Expense
import calendar
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.xlsx"
    budget = get_budget(expense_file_path)
    
    while True:
        # Get user input for expense.
        expense = get_user_expense()
        
        # Save the expense to an Excel file.
        save_expense_to_excel(expense, expense_file_path)
        
        # Summarize the expenses and generate visualizations.
        summarize_expenses(expense_file_path, budget)
        
        # Ask user if they want to continue
        while True:  # Ensures user gives a valid input
            cont = input("\nDo you want to add another expense? (yes/no): ").strip().lower()
            if cont in ['yes', 'no']:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if cont == 'no':
            print("Exiting Expense Tracker. Have a great day!")
            break

def get_budget(expense_file_path):
    try:
        df = pd.read_excel(expense_file_path, sheet_name="Budget")
        budget = float(df.iloc[0, 0])
        print(f"Retrieved saved budget: ₱{budget:.2f}")
    except (FileNotFoundError, ValueError, IndexError):
        while True:
            try:
                budget = float(input("Enter your budget for the month: "))
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        save_budget(expense_file_path, budget)
    return budget

def save_budget(expense_file_path, budget):
    df_budget = pd.DataFrame([budget], columns=["Budget"])
    with pd.ExcelWriter(expense_file_path, engine="xlsxwriter") as writer:
        df_budget.to_excel(writer, index=False, sheet_name="Budget")

def get_user_expense():
    print(f"Getting User Expense...")
    expense_name = input("Enter expense name: ").strip()
    
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
    
    expense_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"You've entered: {expense_name}, ₱{expense_amount:.2f}, {expense_date}")

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
        for i, category in enumerate(expense_category, 1):
            print(f"{i}. {category}")
        
        value_range = f"[1 - {len(expense_category)}]"
        try:
            selected_index = int(input(f"Enter the number of the category {value_range}: ")) - 1
            if 0 <= selected_index < len(expense_category):
                selected_category = expense_category[selected_index]
                print(f"You've selected: {selected_category}")
                return Expense(name=expense_name, category=selected_category, amount=expense_amount, date=expense_date)
            else:
                print("Invalid selection. Please enter a number in the given range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_expense_to_excel(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}...")
    
    try:
        # Load existing Excel file
        with pd.ExcelFile(expense_file_path) as xls:
            sheets = xls.sheet_names
            
            # Load Expenses sheet if exists, otherwise create a new DataFrame
            if "Expenses" in sheets:
                df_expenses = pd.read_excel(xls, sheet_name="Expenses")
            else:
                df_expenses = pd.DataFrame(columns=["Date", "Name", "Amount", "Category"])
            
            # Load Budget sheet if exists, otherwise set a new budget
            if "Budget" in sheets:
                df_budget = pd.read_excel(xls, sheet_name="Budget")
                budget = float(df_budget.iloc[0, 0])  # Retrieve existing budget
            else:
                budget = get_budget(expense_file_path)  # Prompt for new budget
    except FileNotFoundError:
        # If file does not exist, create new DataFrames
        df_expenses = pd.DataFrame(columns=["Date", "Name", "Amount", "Category"])
        budget = get_budget(expense_file_path)

    # Add the new expense to the DataFrame
    new_data = pd.DataFrame({
        "Date": [expense.date],
        "Name": [expense.name], 
        "Amount": [expense.amount], 
        "Category": [expense.category]
    })
    df_expenses = pd.concat([df_expenses, new_data], ignore_index=True)
    
    # Save both sheets back into the file
    with pd.ExcelWriter(expense_file_path, engine="xlsxwriter") as writer:
        df_expenses.to_excel(writer, index=False, sheet_name="Expenses")
        pd.DataFrame([budget], columns=["Budget"]).to_excel(writer, index=False, sheet_name="Budget")
        
        workbook = writer.book
        worksheet = writer.sheets["Expenses"]
        
        format_currency = workbook.add_format({'num_format': '₱#,##0.00'})
        worksheet.set_column("C:C", 12, format_currency)
        worksheet.set_column("A:D", 20)

def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expenses...")
    try:
        df = pd.read_excel(expense_file_path, sheet_name="Expenses")
    except FileNotFoundError:
        print("No expenses recorded yet.")
        return
    
    total_expense = df["Amount"].sum()
    print(f"Total Expense: ₱{total_expense:.2f}")
    
    remaining_budget = budget - total_expense
    print(f"Remaining Budget: ₱{remaining_budget:.2f}")
    
    today = datetime.date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    remaining_days = days_in_month - today.day
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(green(f"It's recommended to spend a daily budget of ₱{daily_budget:.2f} in the remaining days."))
    
    category_summary = df.groupby("Category")["Amount"].sum()
    expense_names = df.groupby("Category")["Name"].apply(lambda x: ', '.join(x))
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(category_summary.index, category_summary.values)
    plt.title("Expenses by Category")
    plt.ylabel("Amount (₱)")
    plt.xticks(rotation=45)
    
    for bar, label in zip(bars, expense_names):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), label, ha='center', va='bottom', fontsize=9, wrap=True)
    
    plt.show()
    input("Press Enter to continue...")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == '__main__':
    main()
