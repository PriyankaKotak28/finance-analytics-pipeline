import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# Config
NUM_TRANSACTIONS = 10000
START_DATE = datetime(2023, 1, 1)

CATEGORIES = {
    'Groceries': ['Woolworths', 'Coles', 'Aldi', 'IGA'],
    'Transport': ['Myki', 'Uber', 'Shell', 'BP'],
    'Dining': ['McDonalds', 'Uber Eats', 'Menulog', 'Nandos'],
    'Entertainment': ['Netflix', 'Spotify', 'Event Cinemas', 'Steam'],
    'Utilities': ['AGL Energy', 'Origin Energy', 'Telstra', 'Optus'],
    'Healthcare': ['Chemist Warehouse', 'Priceline', 'Medibank'],
    'Shopping': ['JB Hi-Fi', 'Kmart', 'Target', 'Amazon AU'],
}

ACCOUNT_IDS = [f'ACC{str(i).zfill(4)}' for i in range(1, 51)]

rows = []
for i in range(NUM_TRANSACTIONS):
    category = random.choice(list(CATEGORIES.keys()))
    merchant = random.choice(CATEGORIES[category])
    date = START_DATE + timedelta(days=random.randint(0, 364))
    amount = round(random.uniform(5, 500), 2)
    # flag high transactions as potential anomalies
    is_anomaly = 1 if amount > 450 else 0

    rows.append({
        'transaction_id': f'TXN{str(i+1).zfill(6)}',
        'account_id': random.choice(ACCOUNT_IDS),
        'date': date.strftime('%Y-%m-%d'),
        'merchant': merchant,
        'category': category,
        'amount': amount,
        'is_anomaly': is_anomaly,
    })

df = pd.DataFrame(rows)
df.to_csv('data/raw_transactions.csv', index=False)
print(f"✅ Generated {len(df)} transactions")
print(df.head())