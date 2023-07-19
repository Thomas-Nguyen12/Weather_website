import pandas as pd 
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

emission = pd.read_csv("greenhouse.csv")
emission.rename({"country_or_area": "country"}, axis=1, inplace=True)
le = LabelEncoder()

emission.country = le.fit_transform(emission.country)



from sklearn.ensemble import RandomForestClassifier



X = emission.drop(["country", "year", "category"], axis=1)
y = emission.country.values.reshape(-1,1)

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(random_state=42)

model.fit(X_train, Y_train)
pred = model.predict(X_test)
accuracy = accuracy_score(Y_test, pred) * 100
