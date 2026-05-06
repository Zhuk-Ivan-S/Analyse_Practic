import pandas as pd

# open file
df_raw = pd.read_csv('../row_files/bronze_credits.csv')

print(df_raw.head(10))
print(df_raw.info())
print(f'Duplicated data: {df_raw.duplicated().value_counts()}') # duplicated info in Data
print(f'Missing values: \n{df_raw.isnull().sum()}') # Missing values

# So many missing values in credit amount - that is very big mistake. I have no possibility to take info from another
# source for example some update or new data . So i try to replace credit amount into average(just for practice)
average_credit_amount = df_raw['amount'].mean()
print(f'Average amount of credit: {average_credit_amount} euros') # badly History !)
df_raw['amount'] = df_raw['amount'].fillna(average_credit_amount) # replace missing values on average
print(f'missing values in amount: {df_raw['amount'].isnull().sum()}')
# NaN in collateral_type - just change into "Nothing"
df_raw['collateral_type'] = df_raw['collateral_type'].fillna('Nothing')
print(df_raw['collateral_type'].unique())

print(f'Missing values: \n{df_raw.isnull().sum()}') # Missing values
df_raw.loc[df_raw['collateral_type'] == 'Nothing', 'collateral_value'] = 0 # for collateral type NONE correct value into 0

# Calculations - EAD
df_raw['collateral_ratio'] = (df_raw['collateral_value'] / df_raw['amount']) * 100
print(df_raw['collateral_ratio'])

df_raw.to_csv('../Training in IRBA/source/silver_credits.csv', index = False)