import pandas as pd

df = pd.read_csv('../Row_files/Global GDP Explorer 2025 (World Bank  UN Data).csv')

print(df.head(10))
print(df.columns)
print(df.isnull().value_counts())
print(df.duplicated().value_counts())
# Data clean and preparing for visualisation and analyse
df['GDP (nominal, 2023)'] = df['GDP (nominal, 2023)'].str.replace('$','')
df['GDP (nominal, 2023)'] = df['GDP (nominal, 2023)'].str.replace(',','')
df['GDP (nominal, 2023)'] = df['GDP (nominal, 2023)'].astype(float)
#print(df['GDP (nominal, 2023)'].head(10))
df['GDP Growth_num'] = df['GDP Growth'].str.replace('%','')
df['GDP Growth_num'] = df['GDP Growth_num'].str.replace('−','-')
df['GDP Growth_num'] = df['GDP Growth_num'].astype(float)
df['GDP Growth_num'] = df['GDP Growth_num'] / 100
#print(df['GDP Growth_num'].head(10))
df['GDP per capita_num'] = df['GDP per capita'].str.replace('$','')
df['GDP per capita_num'] = df['GDP per capita_num'].str.replace(',','')
df['GDP per capita_num'] = df['GDP per capita_num'].astype(float)
#print(df['GDP per capita_num'].head(10))
df['Share of World GDP_num'] = df['Share of World GDP'].str.replace('%','')
df['Share of World GDP_num'] = df['Share of World GDP_num'].astype(float)
print(df['Share of World GDP_num'].head(10))

df.to_csv('../Final_files(clean, prepared or some visualisation)/WorldGDP.csv')


