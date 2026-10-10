"""Model-facing tools for the expense assistant.

@tool derives the schema from the signature and docstring, so these wrappers
take NO arguments: the model must not be asked for the transaction list.
They fetch it themselves and return JSON strings.
"""

import json
from functools import lru_cache
from pathlib import Path

from langchain_core.tools import tool

from expensetracker import report
from expensetracker.loader import load_transactions

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_PATH = PROJECT_ROOT / "expensetracker" / "data.csv"


@lru_cache(maxsize=1)
def _transactions():
    """Load once and reuse. Tuple so lru_cache can hash the result."""
    txns, errors = load_transactions(DATA_PATH)
    return tuple(txns), tuple(errors)


@tool
def summary() -> str:
    """Returns the overall figures: total_income, total_expense and balance
    (income minus expenses), plus a per-category breakdown and the biggest
    expense. This is the only tool that knows about income, so use it for any
    question about income, earnings, salary, balance, or money left over.
    """
    txns, _ = _transactions()
    return json.dumps(report.summary(list(txns)))


@tool
def total_by_category() -> str:
    """Returns how much was spent in each expense category, as a mapping of
    category name (for example, food or travel) to the amount spent. Expenses
    only: this contains no income figure and no overall total.
    """
    txns, _ = _transactions()
    return json.dumps(report.total_by_category(list(txns)))


@tool
def biggest_expense() -> str:
    """Returns the single largest individual expense, as one transaction with
    its date, category, amount, and description. Use this for the biggest or
    most expensive single purchase. This is one transaction, not a category
    total.
    """
    txns, _ = _transactions()
    expense = report.biggest_expense(list(txns))
    return json.dumps(expense.to_dict() if expense else None)


TOOLS = [summary, total_by_category, biggest_expense]
tool_map = {t.name: t for t in TOOLS}