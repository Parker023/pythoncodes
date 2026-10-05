from models import Expense, Income
from loader import load_transactions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def total_by_category(txns):
    totals = {}
    for t in txns:
        if isinstance(t, Expense):
            totals[t.category] = totals.get(t.category, 0) + t.amount
    return totals


def biggest_expense(txns):
    expenses = [t for t in txns if isinstance(t, Expense)]
    if not expenses:
        return None
    return max(expenses, key=lambda t: t.amount)


def summary(txns):
    total_income = sum(txn.amount for txn in txns if isinstance(txn, Income))
    total_expense = sum(txn.amount for txn in txns if isinstance(txn, Expense))
    balance = sum(t.signed_amount() for t in txns)
    biggest_exp = biggest_expense(txns)
    return {"total_income": total_income, "total_expense": total_expense, "balance": balance,"total_by_category": total_by_category(txns), "biggest_expense": biggest_exp.to_dict() if biggest_exp else None ,}


def to_dataframe(txns):
    return pd.DataFrame([{
        "date": t.date,
        "category": t.category,
        "amount": t.amount,
        "description": t.description,
        "type": type(t).__name__,
        "signed": t.signed_amount(),

    } for t in txns])


# if __name__ == "__main__":
#     df = to_dataframe(load_transactions("./data.csv")[0])
#     expenses = df[df["type"] == 'Expense']
#
#     total_by_category=expenses.groupby("category")["amount"].sum()
#     biggest_expense=expenses["amount"].max()
#
#     total_income=df[df["type"] == 'Income']["amount"].sum(axis=0)
#
#     total_expense=expenses["amount"].sum(axis=0)
#     balance=df["signed"].sum(axis=0)
#
#     print("total_by_category: ", total_by_category,)
#     print("********************")
#     print("biggest_expense: ", biggest_expense)
#     print("********************")
#     print("total_income: ", total_income)
#     print("********************")
#     print("total_expense: ", total_expense)
#     print("********************")
#     print("balance: ", balance)
#
#     amounts = expenses["amount"].values
#     mean, std = np.mean(amounts), np.std(amounts)
#     print(f"mean {mean:.2f}  std {std:.2f}  threshold {mean + 2 * std:.2f}")
#     print(expenses[amounts > mean + 2 * std])
#
#
#
#
#     total_by_category.plot(kind="bar", title="Spend by category")
#     plt.ylabel("Amount")
#     plt.tight_layout()
#     plt.savefig("spend.png")
#     plt.show()

