import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.externals import joblib

data = pd.read_csv("ShoppingDatasetFinal.csv")
print(data.head)
#data = data.sample(frac=1).reset_index(drop=True)   #Shuffle
#data.to_csv("ShoppingDatasetFinal.csv")
#data.drop(data.columns[[0]], axis=1)
X = data.iloc[:, 1:30]
X = X.drop(['product','top','set','best','please','detail'], axis=1)
print(X.head)

Y = data.iloc[:, -1]
print(Y.head)

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

print(X_train)
print(X_test)

from xgboost import XGBClassifier
model = XGBClassifier(n_estimators=200, learning_rate=0.05)
model.fit(X_train, Y_train, early_stopping_rounds=5, eval_set=[(X_test, Y_test)], verbose=True)

prediction = model.predict(X_test)

from sklearn.metrics import accuracy_score
result = accuracy_score(prediction, Y_test, normalize=True)
print("Accuracy score: " + str(result))

saveModel = joblib.dump(model, "Shopping_Model_XGBoost.pkl")
