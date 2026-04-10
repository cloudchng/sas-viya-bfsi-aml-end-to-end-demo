import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# Create directories
os.makedirs('data', exist_ok=True)

# Configuration
NUM_CUSTOMERS = 1500
NUM_ACCOUNTS = 1800
NUM_TRANSACTIONS = 75000
START_DATE = datetime(2024, 1, 1)

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# --- Reference Data Creation ---
print("Generating Reference Data...")

# 1. Exclusions (Trusted Entities)
exclusions_data = [
    {'customer_id': 'CUST_TRUST_001', 'Reason': 'Government Entity', 'Date_Added': '2023-01-01'},
    {'customer_id': 'CUST_TRUST_002', 'Reason': 'Interbank Settlement', 'Date_Added': '2023-01-01'},
    {'customer_id': 'CUST_TRUST_003', 'Reason': 'Public Utility', 'Date_Added': '2023-05-15'},
    {'customer_id': 'ACC_EXCL_999', 'Reason': 'Central Bank Operations', 'Date_Added': '2023-02-10'}
]
pd.DataFrame(exclusions_data).to_csv('data/aml_exclusions.csv', index=False)

# 2. Country Risk
country_risk_data = [
    {'Country_Code': 'AF', 'Country_Name': 'Afghanistan', 'Risk_Level': 'High', 'Risk_Score': 95},
    {'Country_Code': 'KP', 'Country_Name': 'North Korea', 'Risk_Level': 'High', 'Risk_Score': 98},
    {'Country_Code': 'IR', 'Country_Name': 'Iran', 'Risk_Level': 'High', 'Risk_Score': 90},
    {'Country_Code': 'SY', 'Country_Name': 'Syria', 'Risk_Level': 'High', 'Risk_Score': 85},
    {'Country_Code': 'KY', 'Country_Name': 'Cayman Islands', 'Risk_Level': 'Medium-High', 'Risk_Score': 75},
    {'Country_Code': 'PA', 'Country_Name': 'Panama', 'Risk_Level': 'Medium-High', 'Risk_Score': 70},
    {'Country_Code': 'CH', 'Country_Name': 'Switzerland', 'Risk_Level': 'Low', 'Risk_Score': 20},
    {'Country_Code': 'SG', 'Country_Name': 'Singapore', 'Risk_Level': 'Low', 'Risk_Score': 15},
    {'Country_Code': 'US', 'Country_Name': 'United States', 'Risk_Level': 'Low', 'Risk_Score': 10},
    {'Country_Code': 'GB', 'Country_Name': 'United Kingdom', 'Risk_Level': 'Low', 'Risk_Score': 12}
]
pd.DataFrame(country_risk_data).to_csv('data/aml_country_risk.csv', index=False)

# 3. PEP List
pep_data = [
    {'PEP_ID': 'PEP_001', 'FullName': 'John Doe Senior', 'Position': 'Minister of Finance', 'Country': 'CA', 'Risk_Level': 'High'},
    {'PEP_ID': 'PEP_002', 'FullName': 'Maria Garcia', 'Position': 'Central Bank Governor', 'Country': 'ES', 'Risk_Level': 'High'},
    {'PEP_ID': 'PEP_003', 'FullName': 'Ahmed Al-Fayed', 'Position': 'Energy Oversight Board', 'Country': 'AE', 'Risk_Level': 'High'},
    {'PEP_ID': 'PEP_004', 'FullName': 'Chen Wei', 'Position': 'Provincial Governor', 'Country': 'CN', 'Risk_Level': 'High'},
    {'PEP_ID': 'PEP_005', 'FullName': 'Elena Rossi', 'Position': 'Ambassador', 'Country': 'IT', 'Risk_Level': 'Medium'}
]
pd.DataFrame(pep_data).to_csv('data/aml_pep_list.csv', index=False)

# --- Core Data Generation ---

print("Generating Enhanced Customers...")
customer_ids = [f"CUST_{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]
segments = ['Retail', 'SME', 'Corporate', 'HNWI']
nationalities = ['USA', 'UK', 'Singapore', 'China', 'Malaysia', 'India', 'Russia', 'KP', 'IR', 'KY']
professions = ['Engineer', 'Doctor', 'Business Owner', 'Unemployed', 'Consultant', 'Politician', 'Student']

profession_income_map = {
    'Engineer': 8000,
    'Doctor': 15000,
    'Business Owner': 50000,
    'Unemployed': 800,
    'Consultant': 10000,
    'Politician': 12000,
    'Student': 500
}

customers = pd.DataFrame({
    'customer_id': customer_ids,
    'name': [f"Customer {i}" for i in range(1, NUM_CUSTOMERS + 1)],
    'segment': [random.choice(segments) for _ in range(NUM_CUSTOMERS)],
    'kyc_risk_rating': [random.randint(1, 10) for _ in range(NUM_CUSTOMERS)],
    'nationality': [random.choice(nationalities) for _ in range(NUM_CUSTOMERS)],
    'profession': [random.choice(professions) for _ in range(NUM_CUSTOMERS)]
})
customers['expected_monthly_turnover'] = customers['profession'].map(profession_income_map)

# Inject some excluded customers
customers.loc[0:2, 'customer_id'] = ['CUST_TRUST_001', 'CUST_TRUST_002', 'CUST_TRUST_003']

print("Generating Accounts...")
account_ids = [f"ACC_{i:05d}" for i in range(1, NUM_ACCOUNTS + 1)]
accounts = pd.DataFrame({
    'account_id': account_ids,
    'customer_id': [random.choice(customer_ids) for _ in range(NUM_ACCOUNTS)],
    'account_type': [random.choice(['Savings', 'Checking', 'Credit Card']) for _ in range(NUM_ACCOUNTS)],
    'open_date': [random_date(START_DATE - timedelta(days=365*5), START_DATE) for _ in range(NUM_ACCOUNTS)],
    'currency': 'USD'
})

print("Generating Transactions...")
tx_data = []
for i in range(1, NUM_TRANSACTIONS + 1):
    tx_type = random.choice(['CASH', 'WIRE', 'ACH', 'ATM'])
    amount = round(random.uniform(10, 5000), 2)
    
    tx_data.append({
        'tx_id': f"TX_{i:07d}",
        'account_id': random.choice(account_ids),
        'tx_date': random_date(START_DATE, START_DATE + timedelta(days=365)),
        'amount': amount,
        'tx_type': tx_type,
        'counterparty_name': f"Counterparty {random.randint(1, 1000)}",
        'counterparty_country': random.choice(nationalities),
        'suspicious_flag': 0,
        'typology': 'Normal'
    })

transactions = pd.DataFrame(tx_data)

# --- Injecting Complex AML Typologies ---

print("Injecting Advanced AML Patterns...")

# 1. Structuring (Smurfing)
smurfer_accs = accounts.sample(10)['account_id'].values
for acc_id in smurfer_accs:
    base_date = START_DATE + timedelta(days=random.randint(10, 300))
    for i in range(10):
        idx = random.randint(0, NUM_TRANSACTIONS - 1)
        transactions.loc[idx, 'account_id'] = acc_id
        transactions.loc[idx, 'tx_date'] = base_date + timedelta(hours=i*3)
        transactions.loc[idx, 'amount'] = round(random.uniform(9000, 9900), 2)
        transactions.loc[idx, 'tx_type'] = 'CASH'
        transactions.loc[idx, 'suspicious_flag'] = 1
        transactions.loc[idx, 'typology'] = 'Structuring'

# 2. Velocity Abuse
velocity_accs = accounts.sample(5)['account_id'].values
for acc_id in velocity_accs:
    base_date = START_DATE + timedelta(days=random.randint(10, 300))
    idx_in = random.randint(0, NUM_TRANSACTIONS - 1)
    transactions.loc[idx_in, 'account_id'] = acc_id
    transactions.loc[idx_in, 'amount'] = 50000
    transactions.loc[idx_in, 'tx_type'] = 'WIRE'
    transactions.loc[idx_in, 'tx_date'] = base_date
    
    idx_out = random.randint(0, NUM_TRANSACTIONS - 1)
    transactions.loc[idx_out, 'account_id'] = acc_id
    transactions.loc[idx_out, 'amount'] = 49950
    transactions.loc[idx_out, 'tx_type'] = 'WIRE'
    transactions.loc[idx_out, 'tx_date'] = base_date + timedelta(minutes=25)
    transactions.loc[idx_out, 'suspicious_flag'] = 1
    transactions.loc[idx_out, 'typology'] = 'Rapid Velocity'

# 3. Income Inconsistency
target_custs = customers[customers['profession'].isin(['Student', 'Unemployed'])].sample(5)['customer_id'].values
target_accs = accounts[accounts['customer_id'].isin(target_custs)]['account_id'].values
for acc_id in target_accs:
    idx = random.randint(0, NUM_TRANSACTIONS - 1)
    transactions.loc[idx, 'account_id'] = acc_id
    transactions.loc[idx, 'amount'] = round(random.uniform(100000, 500000), 2)
    transactions.loc[idx, 'tx_type'] = 'WIRE'
    transactions.loc[idx, 'suspicious_flag'] = 1
    transactions.loc[idx, 'typology'] = 'Income Inconsistency'

# 4. PEP and Country Risk Matches (For Stage 4 Shield)
pep_names = ['John Doe Senior', 'Maria Garcia', 'Ahmed Al-Fayed']
high_risk_countries = ['KP', 'IR', 'AF']

for name in pep_names:
    target_idx = random.sample(list(transactions.index), 10)
    transactions.loc[target_idx, 'counterparty_name'] = name
    transactions.loc[target_idx, 'suspicious_flag'] = 1
    transactions.loc[target_idx, 'typology'] = 'PEP Match'

for country in high_risk_countries:
    population = list(transactions.index[transactions['counterparty_country'] == country])
    sample_size = min(len(population), 50)
    if sample_size > 0:
        target_idx = random.sample(population, sample_size)
        transactions.loc[target_idx, 'suspicious_flag'] = 1
        transactions.loc[target_idx, 'typology'] = 'High Risk Jurisdiction'

# 5. Customer Risk History
print("Generating Risk History...")
risk_history = []
for cust_id in customer_ids:
    base_risk = random.randint(1, 10)
    risk_history.append({'customer_id': cust_id, 'date': START_DATE, 'old_risk': base_risk, 'new_risk': base_risk})
    if random.random() < 0.2:
        risk_history.append({'customer_id': cust_id, 'date': START_DATE + timedelta(days=180), 'old_risk': base_risk, 'new_risk': random.randint(1, 10)})

# Save datasets
customers.to_csv('data/aml_customers.csv', index=False)
accounts.to_csv('data/aml_accounts.csv', index=False)
transactions.to_csv('data/aml_transactions.csv', index=False)
pd.DataFrame(risk_history).to_csv('data/aml_risk_history.csv', index=False)

# Watchlist - OFAC Matches
watchlist_names = ['Terrorism Finance Inc', 'Oligarch Holdings', 'Cartel Logistics']
watchlist = pd.DataFrame({
    'entity_name': watchlist_names,
    'reason': ['Sanctions', 'Wealth Source Unknown', 'Political Risk']
})
watchlist.to_csv('data/aml_watchlist.csv', index=False)

for name in watchlist_names:
    target_idx = random.sample(list(transactions.index), 15)
    transactions.loc[target_idx, 'counterparty_name'] = name
    transactions.loc[target_idx, 'suspicious_flag'] = 1
    transactions.loc[target_idx, 'typology'] = 'Sanctions Match'

# Re-save transactions with sanctions/pep matches
transactions.to_csv('data/aml_transactions.csv', index=False)

print("All End-to-End AML Demo Data (Core + Reference) Generated successfully.")
