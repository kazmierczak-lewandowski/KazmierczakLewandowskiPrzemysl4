import paho.mqtt.client as mqtt
import time
import random
import pigpio
import RPi.GPIO as GPIO

broker_address = "10.104.32.237"
broker_port = 1883
topic_sensor = "sensor/data"
topic_control = "control/led"

led_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

pi = pigpio.pi()
if not pi.connected:
    exit(0)
sensor = pi.spi_open(1, 1000000, 0) # CE1, 1 Mbps, main SPI

def read_sensor():
    c, d = pi.spi_read(sensor, 2)
    temp = 0.0
    if c == 2:
        sign = (d[0] & 0x80) >> 7
        value = (((d[0] & 0x7f) << 8) | d[1]) >> 5
        temp = value * 0.125
        if sign == 1:
            temp = temp * -1
    return temp, random.randint(150, 300) / 10

def publish_data(client):
    temperature, humidity = read_sensor()
    if humidity is not None and temperature is not None:
        payload = f"{temperature:.2f} {humidity:.2f}"
        client.publish(topic_sensor, payload)
        print(f"Opublikowano: {payload}")
    else:
        print("Błąd odczytu z czujnika!")

def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    print(f"Odebrano komendę: {command} z tematu: {msg.topic}")
    
    if command == "ON":
        GPIO.output(led_pin, GPIO.HIGH)
    elif command == "OFF":
        GPIO.output(led_pin, GPIO.LOW)

client = mqtt.Client()
client.on_message = on_message

client.connect(broker_address, broker_port, 60)
client.subscribe(topic_control)
client.loop_start()

try:
    while True:
        publish_data(client)
        time.sleep(5)
except KeyboardInterrupt:
    print("Przerwanie programu przez użytkownika.")
finally:
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
    pi.spi_close(sensor)
    pi.stop()