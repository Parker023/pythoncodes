import json
from expensetracker.loader import load_transactions
from expensetracker.report import summary


def main():
    try:
        txns, errors = load_transactions("./data.csv")
    except FileNotFoundError as e:
        print("data.csv not found - put it next to main.py")
        return

    print(f"Imported: {len(txns)}")
    print(f"Rejected: {len(errors)}")
    for err in errors:
        print(" ", err)
    expense_summary = summary(txns)

    with open("report.json", "w") as f:
        json.dump(expense_summary, f, indent=4)

    print_report(expense_summary, txns)


def print_report(expense_summary, txns):
    print(f"\nTotal income  : {expense_summary['total_income']:.2f}")
    print(f"Total expense : {expense_summary['total_expense']:.2f}")
    print(f"Balance       : {expense_summary['balance']:.2f}")

    total_by_category = expense_summary['total_by_category']
    biggest_expense = expense_summary['biggest_expense']
    print("\nSpend by category:")
    for category, total in total_by_category.items():
        print(f"  {category:8}: {total:.2f}")

    print(f"\nBiggest expense: {biggest_expense}")


if __name__ == "__main__":
    main()
