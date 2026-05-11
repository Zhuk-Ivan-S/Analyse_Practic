import  pandas as pd
import numpy as np
import numpy as np #just for example in calculatiion

df_clients = pd.read_csv('../source/silver_clients.csv')
df_credits = pd.read_csv('../source/silver_credits.csv')
df_risk_data = pd.read_csv('../row_files/risk_reference.csv')
# Create full table
df_Cl_cr = pd.merge(df_credits, df_clients,  on="client_id", how='left')
print(f"After merge: {len(df_Cl_cr)}")
df_full = pd.merge(df_Cl_cr, df_risk_data, on="job", how='left')
print(f'After second: {len(df_full)}')
print(df_full.head(20))
print(df_full['base_pd'].sum())
# LGD creation - ratings for collateral dict
df_full = df_full.fillna(0)
lgd_mapping = {'Real Estate': 0.2, 'Deposit': 0.2, 'Car': 0.4, 'Nothing': 0.8}
df_full['lgd'] = df_full['collateral_type'].map(lgd_mapping)
print(df_full.head(10))
# PD base for clients under 18 years i think pd * 1.2 for example
df_full['base_pd'] = np.where(
    df_full['is_legal'] == False,
    df_full['base_pd'] * 1.2,
    df_full['base_pd']
)
print(df_full['base_pd'].sum())
# df_full['base_pd'] = np.where ( df_full['is_legal'] == False , df_full['base_pd'] * 1.2 , df_full['base_pd']) #ifelse logic
# Create calculation for Reserves in Banks
df_full['reserves_for_bank'] = df_full['base_pd'] * df_full['lgd'] * df_full['amount'] # RISIKOVORSORGE !
print(df_full.head(10))
full = df_full['reserves_for_bank'].sum()
print(f'Total sum for reserves : {full:,.2f} EUR') # total reserves !
print(df_full['amount'].sum())
print(df_full['base_pd'].sum())
print(df_full['lgd'].sum())
# then statistic and analyse )
df_full.to_csv('../source/gold.csv',index=False)