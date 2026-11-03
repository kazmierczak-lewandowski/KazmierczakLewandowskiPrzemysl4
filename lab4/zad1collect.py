import pandas as pd
import time
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

N_SAMPLES = 100
DELAY = 0.2
MIN_DISTANCE = 3.0
MAX_DISTANCE = 100.0

def check_data(df):
    outliers = df[(df["distance"] < MIN_DISTANCE) | (df["distance"] > MAX_DISTANCE)]
    if not outliers.empty:
        print(f"\nWykryto {len(outliers)} błędów grubych (poza zakresem {MIN_DISTANCE}-{MAX_DISTANCE} cm):")
        print(outliers)
        return False
    return True

def collect_data():
    vl, dev = sensor_init()

    while True:
        input("\nNaciśnij Enter, aby rozpocząć pomiar (4 cykle przybliżania i oddalania dłoni)...")
        data = []

        start_time = time.time()
        for i in range(N_SAMPLES):
            distance, _ = read_sensor(vl, dev)
            experiment_time = time.time() - start_time
            data.append([experiment_time, distance])
            print(f"[{i + 1}/{N_SAMPLES}] Time: {experiment_time:.2f} s, Distance: {distance} cm")
            time.sleep(DELAY)

        df = pd.DataFrame(data, columns=["time", "distance"])

        if check_data(df):
            break
        print("Pomiar należy powtórzyć!")

    df.to_csv("data.csv", index=False)

    print(f"\nZapisano {len(df)} pomiarów do pliku data.csv")
    print(f"Czas eksperymentu: {df['time'].iloc[-1]:.2f} s")
    print(f"Odległość min: {df['distance'].min()} cm, max: {df['distance'].max()} cm, średnia: {df['distance'].mean():.2f} cm")
    return df

if __name__ == "__main__":
    collect_data()
