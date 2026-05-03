import pandas as pd

# ── 1. Load raw data ─────────────────────────────────────
df = pd.read_csv('data/raw_transactions.csv')

print("=== BEFORE Cleaning ===")
print(f"date dtype : {df['date'].dtype}")
print(f"Null values:\n{df.isnull().sum()}")

# ── 2. Fix date column (string → real date) ───────────────
df['date'] = pd.to_datetime(df['date'])

# ── 3. Extract useful date parts ─────────────────────────
# Think of these as computed columns in SQL
df['year']        = df['date'].dt.year
df['month']       = df['date'].dt.month
df['month_name']  = df['date'].dt.strftime('%B')   # January, February...
df['week']        = df['date'].dt.isocalendar().week.astype(int)
df['day_of_week'] = df['date'].dt.strftime('%A')   # Monday, Tuesday...
df['quarter']     = df['date'].dt.quarter           # Q1, Q2, Q3, Q4

# ── 4. Flag high-value transactions ──────────────────────
# Business rule: anything over $400 is flagged for review
df['risk_flag'] = df['amount'].apply(
    lambda x: 'HIGH' if x > 400 else 'MEDIUM' if x > 200 else 'LOW'
)

# ── 5. Round amount to 2 decimal places ──────────────────
df['amount'] = df['amount'].round(2)

# ── 6. Standardise text columns ──────────────────────────
df['category'] = df['category'].str.strip().str.title()
df['merchant'] = df['merchant'].str.strip().str.title()

# ── 7. Verify after cleaning ─────────────────────────────
print("\n=== AFTER Cleaning ===")
print(f"date dtype : {df['date'].dtype}")
print(f"\nNew columns added:\n{df.dtypes}")

print("\n=== Sample Transformed Row ===")
print(df.head(3).to_string())

print("\n=== Spend by Month ===")
monthly = (
    df.groupby(['year', 'month', 'month_name'])['amount']
    .agg(total='sum', transactions='count')
    .round(2)
    .reset_index()
    .sort_values(['year', 'month'])
)
print(monthly.to_string())

print("\n=== Risk Flag Distribution ===")
print(df['risk_flag'].value_counts())

# ── 8. Save cleaned data ──────────────────────────────────
df.to_csv('data/cleaned_transactions.csv', index=False)
print("\n✅ Cleaned data saved to data/cleaned_transactions.csv")