import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

df = pd.read_csv('../Row_files/Berlin_crimes.csv')

def check_up(file):
    print(file.head(10))
    print('Duplicates: ', file.duplicated().value_counts())
    print('Missed values: ', file.isnull().value_counts())
    print('Columns name :', file.columns)

check_up(df)

# question 1: What part of berlin is most dangerous ? Use SQL
conn = sqlite3.connect('databaseCrime.db')
df.to_sql('Berlin_crimes',conn,if_exists='replace',index=False)
query = '''SELECT District, SUM(Robbery + Street_robbery +
       Injury + Agg_assault + Threat + Theft + Car + From_car + Bike +
       Burglary + Fire + Arson + Damage + Graffiti + Drugs + Local) AS Total_Crime_Count from Berlin_crimes GROUP BY District ORDER BY Total_Crime_Count
            DESC LIMIT 10'''
df_top_crime_distr = pd.read_sql_query(query,conn)
print(df_top_crime_distr)
# make bar chart for visual effect
plt.bar(df_top_crime_distr['District'], df_top_crime_distr['Total_Crime_Count'])
plt.xticks(rotation=  90)
plt.xlabel('Name of District in Berlin')
plt.ylabel('Count of crimes')
plt.show()

# question 2: What crimes are growing/going low ?
query = '''SELECT Year,Robbery, Street_robbery,
       Injury, Agg_assault, Threat, Theft, Car, From_car, Bike,
       Burglary, Fire, Arson, Damage, Graffiti, Drugs, Local, SUM(Robbery + Street_robbery +
       Injury + Agg_assault + Threat + Theft + Car + From_car + Bike +
       Burglary + Fire + Arson + Damage + Graffiti + Drugs + Local) AS Total_count from Berlin_crimes 
        GROUP BY Year '''
df_crime_change = pd.read_sql_query(query,conn)
print(df_crime_change)

plt.plot(df_crime_change['Year'],df_crime_change['Total_count'])
plt.xlabel('Year')
plt.ylabel('Count of crimes')
plt.title('Timeline of crimes in Berlin (2012 - 2019)')
plt.show()

#Percentage of crimes in different districts

crime_2012 = df_crime_change.loc[df_crime_change['Year'] == 2012].iloc[0]
crime_2019 = df_crime_change.loc[df_crime_change['Year'] == 2019].iloc[0]

#Types of crimes from Dataset
crime_types = ['Robbery', 'Street_robbery', 'Injury', 'Agg_assault', 'Threat', 'Theft', 'Car', 'From_car', 'Bike', 'Burglary', 'Fire', 'Arson', 'Damage', 'Graffiti', 'Drugs', 'Local']

change_percent = (crime_2019[crime_types] - crime_2012[crime_types]) / crime_2012[crime_types] * 100
df_change_results = change_percent.sort_values(ascending=False).round(2)
print(df_change_results.head(5))
print(df_change_results.tail(5))

#Graffiti    196.15  Burglary         -19.12
#Bike        146.67  Street_robbery   -23.91
#Arson        50.00  Injury           -37.71
#Drugs        35.09  From_car         -39.63
#Damage       27.11  Agg_assault      -52.58

# firs impression all insights i make in post LinkedIn and visual in Tableau