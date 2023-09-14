import pandas as pd 
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score 
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

import shap

emission = pd.read_csv("greenhouse.csv")
## Dropping columns

emission.drop(["Unnamed: 0.1",
               "Unnamed: 0.2"], axis=1,
              inplace=True)


## Preprocessing 
from imblearn.over_sampling import RandomOverSampler 
from category_encoders import TargetEncoder 
from category_encoders import WOEEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split 
from category_encoders.cat_boost import CatBoostEncoder
le = LabelEncoder() 
te = TargetEncoder() 
emission["country_encoded"] = le.fit_transform(emission["country"])

X = emission.drop(["country", "capitals", "country_encoded", "Unnamed: 0", "region", "directions"], axis=1)

y = emission["country_encoded"].values.reshape(-1,1)

## Encoding
X = te.fit_transform(X, emission["country_encoded"])
over_sampler = RandomOverSampler()
X, y = over_sampler.fit_resample(X, y)

## Model
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y)

model = RandomForestClassifier(random_state=42, max_depth=8)
model.fit(X_train, Y_train)
pred = model.predict(X_test) 

## Creating a dataframe filled with encoded values
new_emission = X
new_emission["country"] = y 



## Metrics 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import f1_score 
from sklearn.metrics import recall_score 
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import precision_score 
from sklearn.model_selection import cross_val_score 

train_pred = model.predict(X_train) 
train_accuracy = accuracy_score(Y_train, train_pred)
accuracy = accuracy_score(Y_test, pred)
f1 = f1_score(Y_test, pred, average="macro")
recall = recall_score(Y_test, pred, average="macro")
precision = precision_score(Y_test, pred, average="macro")

## Explainability


