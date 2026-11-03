import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv("data.csv")
values = df["distance"].to_numpy()

WINDOW = 5
TRAIN_SIZE = 80

X, y = [], []

for i in range(len(values) - WINDOW):
    X.append(values[i:i + WINDOW])
    y.append(values[i + WINDOW])

X = np.array(X)
y = np.array(y)

split = TRAIN_SIZE - WINDOW

X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

results = pd.DataFrame({"Rzeczywista wartosc": y_test, "Predykcja": predictions.round(2), "Blad": (y_test - predictions).round(2)})
results.to_csv("results.csv", index=False)

mse = mean_squared_error(y_test, predictions)
print("MSE:", round(mse, 4))

joblib.dump(model, "linear_model.pkl")
