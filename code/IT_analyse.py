import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL.XbmImagePlugin import xbm_head

df = pd.read_csv('../Row_files/IT Salary Survey EU  2020.csv')

# Change column names

df.columns = ['Timestamp', 'Age', 'Gender','City', 'Position', 'Total_Yrs_Exp','Yrs_Exp_DE', 'Seniority','Main_Tech',
              'Other_Tech', 'Salary_Brutto', 'Bonus_Stocks', 'Salary_Brutto_Prev','Bonus_Stock_Prev',
              'Vacation_Days','Employment_Status','Contract_Duration','Main_Lang_Work','Company_Size', 'Company_Type',
              'Lost_Job_Covid', 'Kurzarbeit','WFH_Support']


# replace Nan in 0
df['Bonus_Stocks'] = df['Bonus_Stocks'].fillna(0)
print(df['Bonus_Stocks'].head(10))
print(df.head(10))
print(df.columns)
print(df.size)
print(df.info())

# clean with function

def clean_num(x):
    if pd.isna(x):
        return np.nan
    x = str(x)
    x = re.sub(r'[^\d.,]','',x)
    x = x.replace(',','')
    try:
        return float(x)
    except:
        return np.nan

# Salary and Bonus clean

df['Salary_Brutto'] = df['Salary_Brutto'].apply(clean_num)
df['Bonus_Stocks'] = df['Bonus_Stocks'].apply(clean_num)

# Now calculate Total Salary

df['Total_Salary'] = df['Salary_Brutto'] + df['Bonus_Stocks']
print(df['Total_Salary'].head(10))

# Lets make Exploratory analyse - some demographic insights
# Gender  - firs question gender and payment in IT
gender_stats = df.groupby('Gender')['Total_Salary'].median()
print(gender_stats)
# first visual ?
#plt.figure(figsize=(7,6))
#plt.bar(gender_stats.index, gender_stats.values)
#plt.show()

# Take top 5 Cities by count of employees

top_cities = df['City'].value_counts().head(5)
print(top_cities)

# Median exp by Seniority
print(df['Seniority'].unique())
df['Total_Yrs_Exp']  = df['Total_Yrs_Exp'].apply(clean_num)
print(df.groupby('Seniority')['Total_Yrs_Exp'].median())

# Now questions about payment
# Median Payment by City
salary_city = df.groupby('City')['Salary_Brutto'].median().sort_values(ascending = False).head(5)
print(salary_city)

# Median payment by tech
df['Clean_Main_Tech'] = df['Main_Tech'].astype(str).str.split('/').str[0].str.replace(',','').str.strip()

df['Clean_Main_Tech'] = df['Clean_Main_Tech'].replace(['nan','NaN','None',''],np.nan)
df_lang = df.dropna(subset=['Clean_Main_Tech'])
print(df_lang['Clean_Main_Tech'].unique())
top_tech = df_lang['Clean_Main_Tech'].value_counts().head(7).index
print(top_tech)
salary_by_tech = df_lang[df_lang['Clean_Main_Tech'].isin(top_tech)].groupby('Clean_Main_Tech')['Salary_Brutto'].median().sort_values(ascending = False)
print(salary_by_tech.head(10))

# visual for understanding
#plt.figure(figsize=(7,6))
#plt.bar(salary_by_tech.index, salary_by_tech.values)
#plt.show()

# Language ?

print(df['Main_Lang_Work'].unique())
top_lang_in_program = df['Main_Lang_Work'].value_counts()
print(top_lang_in_program.head(5))

# now i want to know correlation
corr_info = df[['Salary_Brutto','Total_Yrs_Exp','Age','Bonus_Stocks']]
print(corr_info.corr())

bins = [18, 24, 29, 34, 39, 49, 70]
labels = ['18-24', '25-29', '30-34', '35-39','40-49','50+']
df['Age_group'] = pd.cut(df['Age'], bins= bins, labels = labels, right= True)
print(df['Age_group'].value_counts())

#save and visual in Power BI
df.to_csv('../Final_files(clean, prepared or some visualisation)/IT_clean.csv')





