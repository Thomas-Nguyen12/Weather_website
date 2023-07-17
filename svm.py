import pandas as pd 
import scipy.stats as stats
from sklearn import svm
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
le = LabelEncoder()
emission = pd.read_csv("greenhouse.csv")
emission.rename({"country_or_area": "country"}, axis=1, inplace=True)
emission["text"] = "Location: " + emission["country"]
unique = emission.country.unique()

emission["country_encoded"] = le.fit_transform(emission["country"])
from sklearn import svm
X = emission.drop(["country", "category", "year", "text", "country_encoded"], axis=1) # X = emission.value
y = emission["country_encoded"].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)
model = svm.SVC(C=0.02, gamma=0.06)
model.fit(X_train, Y_train)
pred = model.predict(X_test)