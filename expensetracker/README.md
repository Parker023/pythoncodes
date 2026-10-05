# Expense Tracker

A small command-line tool that reads transactions from a CSV, validates them, and produces a spend report.

Built as a practice project covering classes and inheritance, abstract base classes, custom exceptions, file handling, CSV/JSON, dictionaries, and pandas/NumPy/matplotlib.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cd expensetracker
python main.py
```

## Output

```
Imported: 4
Rejected: 2
  Error on row 3: Amount must be a number: 'abc'
  Error on row 6: Amount must be greater than zero.

Total income  : 45000.00
Total expense : 4000.00
Balance       : 41000.00

Spend by category:
  food    : 1500.00
  travel  : 2500.00

Biggest expense: {'date': '2026-01-07', 'amount': 2500.0, ...}
```

Also writes `report.json`.

## Files

| File | Purpose |
|---|---|
| `models.py` | `Transaction` (abstract) with `Expense` and `Income` subclasses, plus `InvalidTransactionError` |
| `loader.py` | Reads the CSV and builds objects, collecting errors instead of crashing |
| `report.py` | Totals, biggest expense, summary, and a DataFrame bridge for analytics |
| `main.py` | Entry point — loads, reports, writes `report.json` |
| `data.csv` | Sample input, including deliberately bad rows |

## How it handles bad data

Validation lives in `Transaction.__init__`, so an invalid object can never be constructed:

- Non-numeric amounts (`abc`) raise `InvalidTransactionError`
- Zero and negative amounts are rejected
- Categories are normalised with `.strip().lower()`, so `"  Food  "` and `"food"` are the same category

`load_transactions` catches these per row, so one bad line doesn't abort the import. Rejected rows are returned alongside the valid ones and reported to the user.

Rows with a `salary` category become `Income`; everything else becomes an `Expense`. The balance is `sum(t.signed_amount())`, where `Expense` returns a negative value and `Income` a positive one.

## Input format

```csv
date,amount,category,description
2026-01-05,1200,Food,Lunch
2026-01-10,45000,Salary,Monthly salary
```

## Possible next steps

- Store transactions in SQLite instead of re-reading the CSV
- Expose the report through a FastAPI endpoint
- Add a Streamlit dashboard for the chart
