import pandas as pd
import numpy as np
import random

np.random.seed(99) # random seed for static random creation (just for my comfort)

# Clients generation 15-20 Professions and +/- 15 Cities
jobs = ['Manager', 'Driver', 'IT Specialist', 'Engineer', 'Student', 'Pensioner', 'Director',
        'Unemployed' , 'Sportsman' , 'Seller','Brewer' , 'Teacher' , 'Security' , 'Police worker']
cities = ['Berlin', 'Baden-Baden','Offenburg','Schramberg', 'Tuttlingen' , 'Dunningen' , 'Frankfurt','Bratslaw',
          'Munich', 'Hamburg', 'Frankfurt', '  Stuttgart', 'Hardt' , 'VS','Rottweil','Sulgen']
# Client base creation
clients_data = {
    'client_id': range(1, 1001), # 1000 clients in 1 file (table)
    'name': [f"Client_{i}" for i in range(1, 1001)], # name creation
    'age': [random.randint(16, 75) for _ in range(1000)], # try to add clients AGE<18
    'job': [random.choice(jobs) for _ in range(1000)], # jobs for clients appropriation
    'city': [random.choice(cities) for _ in range(1000)] # city for clients appropriation
}
collateral_types = ['Real Estate', 'Car', 'Deposit', 'None'] # collateral - very important !

df_clients = pd.DataFrame(clients_data) # DataFrame creation from random source !

# Try to appropriate dirty data - spaces or different cases low / height
df_clients.loc[::10, 'name'] = df_clients['name'].str.upper() + "   " # spaces and Uppercase for names
df_clients.loc[::15, 'city'] = df_clients['city'].str.lower().str.strip() # city in lowercase

# Credits generation
credits_data = {
    'credit_id': [f'CR_{i}' for i in range(1, 1501)],  # credits 1500
    'client_id': [random.randint(1, 1000) for _ in range(1500)], # Some clients have more as 1 credit
    'amount': [random.choice([500, 1000, 5000, 10000, 25000, 50000, np.nan]) for _ in range(1500)], # Credit amount
    'duration': [random.choice([6, 12, 24, 36, 60]) for _ in range(1500)], # duration of credits
    'status': [random.choice(['Active', 'Closed', 'Default']) for _ in range(1500)], # Credit status
    'collateral_type': [random.choice(collateral_types) for _ in range(1500)], # take collaterals for clients
    'collateral_value': [0 for _ in range(1500)] # !!! that was very hard - I use AI for correction :(
}

df_credits = pd.DataFrame(credits_data)
# Collaterals logic: kein)  — 0, if exist — from 50% tо 150% from credit amount
def generate_collateral_value(row):
    if row['collateral_type'] == 'None':
        return 0
    if pd.isna(row['amount']):
        return 0
    return round(row['amount'] * random.uniform(0.5, 1.5), 2) # realize cost of collaterals

df_credits['collateral_value'] = df_credits.apply(generate_collateral_value, axis=1) # column with collateral amount creation
 # in credits Data Frame
# Risc table - here i want to create something like a credit score
# PD - default depends on  Profession
risk_map = {
    'Manager' : 0.05, 'Driver' : 0.12, 'IT Specialist': 0.02,
    'Engineer': 0.03, 'Student': 0.25, 'Pensioner': 0.08, 'Director': 0.01 ,
    'Unemployed' : 0.30 , 'Sportsman' : 0.08, 'Seller' : 0.06,'Brewer' :0.04, 'Teacher': 0.02, 'Security': 0.09,
    'Police worker':0.04
}
df_risk_ref = pd.DataFrame(list(risk_map.items()), columns=['job', 'base_pd'])

# File save
df_clients.to_csv('../Training in IRBA/row_files/bronze_clients.csv', index=False)
df_credits.to_csv('../Training in IRBA/row_files/bronze_credits.csv', index=False)
df_risk_ref.to_csv('../Training in IRBA/row_files/risk_reference.csv', index=False)

print("Training files are ready !") #Logging