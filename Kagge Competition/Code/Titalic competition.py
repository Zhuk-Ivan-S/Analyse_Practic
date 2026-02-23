import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import  RandomForestClassifier
from sklearn.metrics import accuracy_score

gender_value = pd.read_csv("../Row Files/gender_submission.csv")
gender = pd.DataFrame(gender_value)
print(gender.head(10))

train = pd.read_csv("../Row Files/train.csv")
train_base = pd.DataFrame(train)
print(train_base.head(10))
print(train_base.isnull().sum())
print(train_base.duplicated().sum())

test_source = pd.read_csv("../Row Files/test.csv")
test = pd.DataFrame(test_source)
print(test.head(10))
print(test.isnull().sum())
print(test.duplicated().sum())

# Clean data
fill_age = train_base['Age'].median()
train_base['Age'] = train_base['Age'].fillna(fill_age)
test['Age'] = test['Age'].fillna(fill_age)
# Embarked replace missing value by mode
train_base['Embarked'] = train_base['Embarked'].replace({'S':0,'C':1,'Q': 2})
train_base['Embarked'] = train_base['Embarked'].fillna(train_base['Embarked'].median())
test['Embarked'] = test['Embarked'].replace({'S':0,'C':1,'Q': 2})
# Fare fill missing value
test['Fare'] = test['Fare'].fillna(train['Fare'].mean())

test['Sex'] = test['Sex'].replace('male',0)
test['Sex'] = test['Sex'].replace('female',1)
train_base['Sex'] = train_base['Sex'].replace('male',0)
train_base['Sex'] = train_base['Sex'].replace('female',1)
train_base['Sex'] = train_base['Sex'].astype(int)
test['Sex'] = test['Sex'].astype(int)

# clean 'cabin' - just delete missing column
test = test.drop('Cabin', axis=1)
train_base = train_base.drop('Cabin',axis=1)

print(test.isnull().sum())
print(train_base.isnull().sum())

# prediction

basis = ['Pclass','Sex','Age','SibSp','Fare','Parch','Embarked']
X = train_base[basis]
y = train_base['Survived']
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size= 0.2, random_state= 9 )
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X_train,y_train)
prediction = model.predict(X_value)
accuracy = accuracy_score(y_value,prediction)

print(f'Accuracy = {accuracy:.2%}')
X_test = test[basis]
final = model.predict(X_test)

files = pd.DataFrame({'PassengerId' : test.PassengerId, 'Survived': final})
files.to_csv('result_Titanic.csv', index=False)
print('File "Results" are ready')



