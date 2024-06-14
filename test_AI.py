import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from category_encoders import TargetEncoder
import pickle
import shap
from catboost import CatBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import lime 
from lime import lime_tabular
import re
import joblib
# Load data
emission = pd.read_csv("greenhouse.csv", index_col=0)

# Drop unnecessary columns
columns_to_drop = [col for col in emission.columns if re.match(r'Unnamed: \d+', col)]
emission.drop(columns=columns_to_drop, inplace=True)

# Encode categorical data
le = LabelEncoder()
te = TargetEncoder()
emission["country_encoded"] = le.fit_transform(emission["country"])

X = emission.drop(["country", "capitals", "country_encoded", "region", "directions"], axis=1)
y = emission["country_encoded"]
joblib.dump(emission, "emission.pkl")
# Target encoding and oversampling
X = te.fit_transform(X, y)
over_sampler = RandomOverSampler()
X, y = over_sampler.fit_resample(X, y)

# Model training
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y)
model = RandomForestClassifier(max_depth=10)
model.fit(X_train, Y_train)

# Save the trained model
joblib.dump(model, "weather_model.pkl")
# Predictions and metrics
pred = model.predict(X_test)



train_pred = model.predict(X_train)
# Metrics
train_accuracy = accuracy_score(Y_train, train_pred)
accuracy = accuracy_score(Y_test, pred)
f1 = f1_score(Y_test, pred, average="macro")
recall = recall_score(Y_test, pred, average="macro")
precision = precision_score(Y_test, pred, average="macro")

with open("train_accuracy.pkl", "wb") as f:
        pickle.dump(train_accuracy, f)
with open("accuracy.pkl", "wb") as f:
        pickle.dump(accuracy, f)
with open("f1.pkl", "wb") as f:
        pickle.dump(f1, f)
with open("recall.pkl", "wb") as f:
        pickle.dump(recall, f)
with open("precision.pkl", "wb") as f:
        pickle.dump(precision, f)

print(f"Train Accuracy: {train_accuracy}")
print(f"Test Accuracy: {accuracy}")
print(f"F1 Score: {f1}")
print(f"Recall: {recall}")
print(f"Precision: {precision}")


# LIME explainability


# SHAP explainability
explainer = shap.Explainer(model)
shap_values = explainer(X_test)
joblib.dump(explainer, "explainer.pkl")
# Save SHAP values
joblib.dump(shap_values, "weather_shap_values.pkl")
