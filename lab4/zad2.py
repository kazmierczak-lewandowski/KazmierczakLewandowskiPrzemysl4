from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import joblib

df = pd.read_csv("data.csv")
values = df["distance"].to_numpy()

TRAIN_SIZE = 80


def tree_forecast(window, horizon):
    X, y = [], []
    for i in range(len(values) - window):
        X.append(values[i:i + window])
        y.append(values[i + window])

    X = np.array(X)
    y = np.array(y)

    split = TRAIN_SIZE - window

    X_train, y_train = X[:split], y[:split]

    tree = DecisionTreeRegressor(max_depth=4, random_state=42)
    tree.fit(X_train, y_train)

    real, predicted, starts = [], [], []
    for t in range(TRAIN_SIZE, len(values) - horizon + 1):
        history = list(values[t - window:t])
        forecast = []
        for _ in range(horizon):
            next_value = tree.predict(np.array([history[-window:]]))[0]
            forecast.append(next_value)
            history.append(next_value)
        starts.append(t)
        real.append(values[t:t + horizon])
        predicted.append(forecast)

    real = np.array(real)
    predicted = np.array(predicted)

    results = pd.DataFrame({
        "Start": starts,
        "Rzeczywiste wartosci": [list(np.round(r, 2)) for r in real],
        "Predykcja": [list(np.round(p, 2)) for p in predicted],
    })
    print(f"\nOkno: {window}, horyzont: {horizon}")
    print(results.to_string(index=False))

    mse = mean_squared_error(real.flatten(), predicted.flatten())
    mse_steps = [mean_squared_error(real[:, k], predicted[:, k]) for k in range(horizon)]
    print("MSE:", round(mse, 4))
    print("MSE dla kolejnych krokow:", [round(m, 4) for m in mse_steps])

    joblib.dump(tree, f"tree_model_w{window}_h{horizon}.pkl")
    return mse, mse_steps


if __name__ == "__main__":
    summary = []
    for window in [5, 10]:
        for horizon in [1, 3, 5]:
            mse, mse_steps = tree_forecast(window, horizon)
            summary.append({"Okno": window, "Horyzont": horizon, "MSE": round(mse, 4), "MSE ostatniego kroku": round(mse_steps[-1], 4)})

    summary = pd.DataFrame(summary)
    print("\nPodsumowanie:")
    print(summary.to_string(index=False))
    summary.to_csv("tree_results.csv", index=False)
