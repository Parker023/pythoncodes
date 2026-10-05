from abc import ABC, abstractmethod


class InvalidTransactionError(Exception):
    pass


class Transaction(ABC):
    def __init__(self, date: str, amount: float, category: str, description: str):

        try:
            amount = float(amount)
        except (ValueError, TypeError) as e:
            raise InvalidTransactionError(f"Amount must be a number: {amount!r}")
        if amount <= 0:
            raise InvalidTransactionError("Amount must be greater than zero.")
        self.date = date
        self.amount = amount
        self.category = category.strip().lower()
        self.description = description

    @abstractmethod
    def signed_amount(self):
        pass

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "type": type(self).__name__,
        }

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount} | {self.description}"

    def __repr__(self):
        return str(
            {"date": self.date, "amount": self.amount, "category": self.category, "description": self.description})


class Expense(Transaction):

    def signed_amount(self):
        return -self.amount


class Income(Transaction):
    def signed_amount(self):
        return self.amount


def main():
    # e1=Expense("2026-01-09", -50, "Shopping", "x")
    # e2=Expense("2026-01-08", 300, "  food  ", "x")
    e3 = Expense("2026-01-05", 1200, "Food", "x")
    income = Income("2026-01-06", 1000, "Salary", "x")

    # print(e2.category)
    print(e3.signed_amount())
    print(e3)
    print(income.signed_amount())


if __name__ == "__main__":
    main()
