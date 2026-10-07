"""Tool definitions for the expense-tracker tool-calling exercise.

Exposes two objects that must stay in sync:

- ``tools``: the JSON schemas sent to the model, describing each tool's name,
  purpose and parameters so the model can decide when to call it.
- ``tool_map``: maps each tool name to the Python function that implements it.
  The caller uses this to run whatever tool the model asked for.

Every tool here wraps a report function from ``expensetracker.report`` and
takes no arguments from the model; the caller passes in the loaded
transactions itself.

Return convention: every function in ``tool_map`` returns something
``json.dumps`` can serialise, so the caller can send results to the model
without knowing which tool produced them. ``expensetracker.report`` returns a
domain object for the biggest expense, so it is adapted below rather than
changing the report module.
"""

from expensetracker.report import biggest_expense, summary, total_by_category


def biggest_expense_as_dict(txns):
    """``report.biggest_expense`` as a JSON-serialisable dict (None if no expenses)."""
    expense = biggest_expense(txns)
    return expense.to_dict() if expense else None


# Tool name (as the model sees it) -> function that runs it.
tool_map = {
    "biggest_expense": biggest_expense_as_dict,
    "total_by_category": total_by_category,
    "summary": summary,
}


def no_params():
    """An empty-object parameter schema: these tools take no model arguments.

    Returns a new dict each call so the tools never share one object - adding a
    parameter to one tool must not silently add it to the others.
    """
    return {"type": "object", "properties": {}, "required": []}


# Schemas passed to ollama.chat(tools=...). Each "name" must be a key in
# tool_map. The "description" is the ONLY thing the model knows about a tool, so
# each one states what it returns and, where they could be confused, what it
# does not cover.
tools = [
    {
        "type": "function",
        "function": {
            "name": "summary",
            "description": (
                "Returns the overall figures: total_income, total_expense and "
                "balance (income minus expenses), plus a per-category breakdown "
                "and the biggest expense. This is the only tool that knows "
                "about income, so use it for any question about income, "
                "earnings, salary, balance, or money left over."
            ),
            "parameters": no_params(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "total_by_category",
            "description": (
                "Returns how much was spent in each expense category, as a "
                "mapping of category name (for example food or travel) to the "
                "amount spent. Expenses only: this contains no income figure "
                "and no overall total."
            ),
            "parameters": no_params(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "biggest_expense",
            "description": (
                "Returns the single largest individual expense, as one "
                "transaction with its date, category, amount and description. "
                "Use this for the biggest or most expensive single purchase. "
                "This is one transaction, not a category total."
            ),
            "parameters": no_params(),
        },
    },
]
