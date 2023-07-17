import pandas as pd 
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import tensorflow as tf
from tensorflow.keras.layers import Flatten
from tensorflow.keras.utils import to_categorical


df = pd.read_csv("greenhouse.csv")
df.rename({"country_or_area": "country"}, axis=1, inplace=True)
le = LabelEncoder()
df["category_encoded"] = le.fit_transform(df["category"])
df["country_encoded"] = le.fit_transform(df["country"])
df.country_encoded= le.fit_transform(df.country)
X = df.drop(["country", "category", "country_encoded"], axis=1) ## X contains values and year and category
y = df["country_encoded"].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)

model = Sequential()


model.add(Dense(units=43, activation="relu", input_dim=len(X_train.columns)))
for i in range(20):
    model.add(Dense(units=200, activation="relu"))
model.add(Dense(units=100, activation="relu"))
model.add(Dense(units=50, activation="relu"))
## The final output should be a prediction across 43 classes
model.add(Dense(43, activation="softmax"))
y_train_encoded = to_categorical(Y_train, num_classes=43)


model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics = "accuracy")
model.fit(X_train, y_train_encoded, epochs=2000, batch_size=128)

