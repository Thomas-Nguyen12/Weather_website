import pandas as pd 
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score 


emission = pd.read_csv("greenhouse.csv")

X = emission.drop(["country", "country_encoded", "category", "region", "directions", "capitals", 
             "capitals_encoded", "official_language", "region_encoded", "directions_encoded",
             "Unnamed: 0"], axis=1)
y = emission.country_encoded.values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, Y_train)
pred = model.predict(X_test)
print (f"accuracy: {accuracy_score(Y_test, pred) * 100} %")
accuracy = accuracy_score(Y_test, pred) * 100
print ("X columns:")
print (X_train.columns)