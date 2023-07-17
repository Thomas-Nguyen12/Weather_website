import pandas as pd 
import scipy.stats as stats
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
le = LabelEncoder()
emission = pd.read_csv("greenhouse.csv")
emission.rename({"country_or_area": "country"}, axis=1, inplace=True)
emission["text"] = "Location: " + emission["country"]
unique = emission.country.unique()

emission["country"] = le.fit_transform(emission["country"])

X = emission.drop(["country", "category", "year", "text"], axis=1) # X = emission.value
y = emission["country"].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, Y_train)
pred = model.predict(X_test)
accuracy = accuracy_score(Y_test, pred) * 100

