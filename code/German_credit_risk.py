import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('../Row_files/german_credit_data - Copy.csv')

print(df.info())
print(df.size)
print(df.duplicated().sum())
print(df.isnull().sum())
print(df.columns)
print(df.head(10))
print(df['Checking account'].unique())

# 1 Classification

df['Infraction_Type'] = np.where(
    (df['Checking account'] == 'little') & (df['Credit amount'] >= 10000),
    'Financial Red Flag',
    'Normal'
)

print(df['Infraction_Type'].head(10))


def calculate_risk(row):
    score = 0

    if row['Infraction_Type'] == 'Financial Red Flag':
        score += 50
    elif row['Infraction_Type'] == 'Admin Infraction':
        score += 15
    if row['Housing'] == 'free':
        score += 10
    if row['Housing'] == 'rent':
        score += 5

    return score

df['Risk_Score'] = df.apply(calculate_risk, axis=1)
print(df['Risk_Score'])
top20risk = df['Risk_Score'].sort_values(ascending = False).head(20)
print(top20risk)


def calc_hausrate(row):
    score = 0
    if row['Housing'] == 'own':
        score += 1
    elif row['Housing'] == 'rent':
        score += 2
    else: score += 3
    return score

df['House_rate']  = df.apply(calc_hausrate, axis = 1)

print(df['House_rate'].head(10))

corelation = df[['House_rate','Risk_Score']].corr()

print(corelation)

def att_rate(row):

    if row['Risk_Score'] >= 50:
        att = 'Critical'
    elif 10 <= row['Risk_Score'] <= 49:
        att = 'Need attetion'
    else: att = 'Normal'
    return att

df['Attention'] = df.apply(att_rate, axis= 1)
print(df['Attention'])

count = df['Attention'].value_counts()
print(count)

count.plot(kind = 'pie')
plt.show()