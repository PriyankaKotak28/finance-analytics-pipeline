import pandas as pd # type: ignore
from sqlalchemy import create_engine, text # type: ignore

# ── 1. Load cleaned data ──────────────────────────────────
df = pd.read_csv('data/cleaned_transactions.csv')
df['date'] = pd.to_datetime(df['date'])
print(f"📂 Loaded {len(df):,} rows from cleaned CSV")

# ── 2. PostgreSQL connection ──────────────────────────────
# Default PostgreSQL setup — change password to yours
DB_USER     = 'postgres'        # default postgres username
DB_PASSWORD = 'Priraj2805#'   # ← whatever you set during install
DB_HOST     = 'db.firofnlsgbeljlsnxvnp.supabase.co'
DB_PORT     = '5432'            # default postgres port
DB_NAME     = 'postgres'

connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ── 3. Create engine + test connection ────────────────────
try:
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print(f"✅ Connected to PostgreSQL")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# ── 4. Load data into PostgreSQL ──────────────────────────
try:
    df.to_sql(
        name      = 'transactions',
        con       = engine,
        if_exists = 'replace',
        index     = False,
        chunksize = 500
    )
    print(f"✅ Loaded {len(df):,} rows into finance_analytics.transactions")
except Exception as e:
    print(f"❌ Load failed: {e}")
    exit()

# ── 5. Verify ─────────────────────────────────────────────
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM transactions")).scalar()
    print(f"✅ Verified: {count:,} rows in PostgreSQL")

    print("\n=== Sample from PostgreSQL ===")
    sample = pd.read_sql("SELECT * FROM transactions LIMIT 5", conn)
    print(sample.to_string())

    print("\n=== Category Totals ===")
    query = """
        SELECT 
            category,
            COUNT(*)            AS transaction_count,
            ROUND(SUM(amount)::numeric,2)  AS total_spend,
            ROUND(AVG(amount)::numeric,2)  AS avg_spend
        FROM transactions
        GROUP BY category
        ORDER BY total_spend DESC
    """
    summary = pd.read_sql(query, conn)
    print(summary.to_string())