import os
os.system('cls' if os.name == 'nt' else 'clear')  # clears terminal first

import pandas as pd

# ── 1. Load ──────────────────────────────────────────────
df = pd.read_csv('data/raw_transactions.csv')

# ── 2. Basic shape ───────────────────────────────────────
print("=== Shape ===")
print(f"Rows: {df.shape[0]:,}  |  Columns: {df.shape[1]}")

# ── 3. Column types ──────────────────────────────────────
print("\n=== Column Types ===")
print(df.dtypes)

# ── 4. First look ────────────────────────────────────────
print("\n=== First 5 Rows ===")
print(df.head())

# ── 5. Summary stats ─────────────────────────────────────
print("\n=== Amount Stats ===")
print(df['amount'].describe().round(2))

# ── 6. Nulls check ───────────────────────────────────────
print("\n=== Null Values ===")
print(df.isnull().sum())

# ── 7. Unique counts ─────────────────────────────────────
print("\n=== Unique Counts ===")
print(f"Accounts   : {df['account_id'].nunique()}")
print(f"Merchants  : {df['merchant'].nunique()}")
print(f"Categories : {df['category'].nunique()}")

# ── 8. Spend by category ─────────────────────────────────
print("\n=== Total Spend by Category ===")
category_summary = (
    df.groupby('category')['amount']
    .agg(total='sum', avg='mean', count='count')
    .round(2)
    .sort_values('total', ascending=False)
)
print(category_summary)