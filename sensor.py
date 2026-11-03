import ctypes
from time import sleep

GAIN = 6

def sensor_init():
    vl = ctypes.CDLL("/home/pi/vl6180_pi/libvl6180_pi.so")
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
    # print(f"Distance: {dist} mm, Light: {light:.2f}")
    return dist, light