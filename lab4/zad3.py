import time
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes
from time import sleep

GAIN = 6

def sensor_init():
    vl = ctypes.CDLL("/usr/local//lib/libvl6180_pi.so")
    vl.vl6180_initialise.argtypes = [ctypes.c_int]
    vl.vl6180_initialise.restype = ctypes.c_void_p
    vl.get_distance.argtypes = [ctypes.c_void_p]
    vl.get_distance.restype = ctypes.c_int
    vl.get_ambient_light.argtypes = [ctypes.c_void_p, ctypes.c_int]
    vl.get_ambient_light.restype = ctypes.c_float
    dev = vl.vl6180_initialise(0)
    return vl, dev


def read_sensor(vl, dev):
    dist = vl.get_distance(dev)
    light = vl.get_ambient_light(dev, GAIN)
    return dist, light

WINDOW = 5
DELAY = 0.2
VISIBLE_POINTS = 100

linear_model = joblib.load("linear_model.pkl")
tree_model = joblib.load("tree_model_w5_h1.pkl")


def predict_next(history):
    x = np.array([history[-WINDOW:]])
    return linear_model.predict(x)[0], tree_model.predict(x)[0]


def running_mse(real, pred):
    real = np.array(real)
    pred = np.array(pred)
    mask = ~np.isnan(pred)
    if not mask.any():
        return float("nan")
    return np.mean((real[mask] - pred[mask]) ** 2)


def main():
    vl, dev = sensor_init()

    times, real, pred_lin, pred_tree = [], [], [], []
    next_lin, next_tree = np.nan, np.nan

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 5))
    line_real, = ax.plot([], [], "o-", color="black", markersize=3, label="Rzeczywisty pomiar")
    line_lin, = ax.plot([], [], "s--", color="tab:blue", markersize=3, label="Regresja liniowa")
    line_tree, = ax.plot([], [], "^--", color="tab:orange", markersize=3, label="Drzewo decyzyjne")
    next_lin_marker, = ax.plot([], [], "s", color="tab:blue", markersize=9, markerfacecolor="none")
    next_tree_marker, = ax.plot([], [], "^", color="tab:orange", markersize=9, markerfacecolor="none")
    ax.set_xlabel("Czas [s]")
    ax.set_ylabel("Odległość [cm]")
    ax.grid(True)
    ax.legend(loc="upper left")

    start_time = time.time()
    try:
        while plt.fignum_exists(fig.number):
            distance, _ = read_sensor(vl, dev)
            experiment_time = time.time() - start_time

            times.append(experiment_time)
            real.append(distance)
            pred_lin.append(next_lin)
            pred_tree.append(next_tree)

            if len(real) >= WINDOW:
                next_lin, next_tree = predict_next(real)

            t = times[-VISIBLE_POINTS:]
            line_real.set_data(t, real[-VISIBLE_POINTS:])
            line_lin.set_data(t, pred_lin[-VISIBLE_POINTS:])
            line_tree.set_data(t, pred_tree[-VISIBLE_POINTS:])
            next_time = experiment_time + DELAY
            next_lin_marker.set_data([next_time], [next_lin])
            next_tree_marker.set_data([next_time], [next_tree])

            ax.set_title(f"MSE regresja liniowa: {running_mse(real, pred_lin):.2f}, "
                         f"MSE drzewo: {running_mse(real, pred_tree):.2f}")
            ax.relim()
            ax.autoscale_view()
            ax.set_xlim(t[0], next_time + DELAY)

            plt.pause(DELAY)
    except KeyboardInterrupt:
        pass

    df = pd.DataFrame({"time": times, "distance": real, "linear": pred_lin, "tree": pred_tree})
    df.to_csv("realtime.csv", index=False)
    fig.savefig("realtime.png", dpi=150)
    print(f"\nMSE regresja liniowa: {running_mse(real, pred_lin):.4f}")
    print(f"MSE drzewo decyzyjne: {running_mse(real, pred_tree):.4f}")

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
