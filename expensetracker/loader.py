import csv

from models import Income, Expense, InvalidTransactionError


def load_transactions(path: str):
    transactions = []
    errors = []

    with open(path, "r") as file:
        reader = csv.DictReader(file)
        for row, data in enumerate(reader, start=2):
            try:
                category = data["category"].strip().lower()
                if category == "salary":
                    transactions.append(
                        Income(data["date"], data["amount"], category, data["description"]))
                else:
                    transactions.append(
                        Expense(data["date"], data["amount"], category, data["description"]))
            except InvalidTransactionError as e:
                errors.append(f"Error on row {row}: {e}")
            except (AttributeError, KeyError):
                errors.append(f"Error on row {row}: malformed row {data}")

    return transactions, errors


if __name__ == "__main__":
    result=load_transactions("./data.csv")


