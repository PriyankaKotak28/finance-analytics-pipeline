# incase supabase is not connecting with POWER BI 

import pandas as pd # type: ignore
from sqlalchemy import create_engine, text # type: ignore

DB_USER     = 'postgres'
DB_PASSWORD = 'Priraj2805#'
DB_HOST     = 'db.firofnlsgbeljlsnxvnp.supabase.co'
DB_PORT     = '5432'
DB_NAME     = 'postgres'

connection_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)

with engine.connect() as conn:
    # Export full transactions
    df = pd.read_sql("SELECT * FROM transactions", conn)
    df.to_csv('data/powerbi_transactions.csv', index=False)
    print(f"✅ Exported {len(df):,} rows to data/powerbi_transactions.csv")