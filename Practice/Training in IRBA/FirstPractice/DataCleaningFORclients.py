import  pandas as pd

# Start of cleaning

df_raw = pd.read_csv('../row_files/bronze_clients.csv') # open file and transform into DATAFRAME
print(df_raw.head(10)) # first looking

#Piplene creation
# first of all looking for missing values and duplicates
print(df_raw.info())
print(f'Duplicates: {df_raw.duplicated().value_counts()}')
print(f'Missing values: \n{df_raw.isnull().sum()}')
print(df_raw['city'].unique()) # no Unknown cities or something else
print(df_raw['job'].unique()) # same
print(df_raw['age'].unique())

# Normalization for all info - lower upper case - for name and city , delete spaces in names
df_clean = df_raw.copy() # save original data
df_clean['name'] = df_raw['name'].str.title().str.strip() # All in title and delete spaces
df_clean['city'] = df_raw['city'].str.title().str.strip()
# DataFrame has info about clients with age under 18 years - create new column with calculation of legalize
df_clean['is_legal'] = df_clean['age'] >= 18 # True - legal / False - not
print(df_clean.head(10))

df_clean.to_csv('../Training in IRBA/source/silver_clients.csv', index = False)