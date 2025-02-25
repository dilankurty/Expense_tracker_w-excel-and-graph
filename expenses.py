class Expense:
    def __init__(self, name, category, amount, date):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"Expense(name={self.name}, category={self.category}, amount={self.amount}, date={self.date})"
