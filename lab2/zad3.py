import paho.mqtt.client as mqtt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import datetime
import time
broker_address = "10.104.32.237"
broker_port = 1883
topic = "sensor/data"
topic_control = "control/led"
fig, ax = plt.subplots()
times = []
humidity = []
temps = []

def on_message(client, userdata, message):
  payload = message.payload.decode("utf-8")
  temp, hum = map(float, payload.split(" "))

  times.append(datetime.datetime.now())
  humidity.append(hum)
  temps.append(temp)

  if len(times) > 5:
    times.pop(0)
    humidity.pop(0)
    temps.pop(0)

  print(f"Temperature: {temp} | Humidity: {hum}")


def chart(i):
    ax.clear()
    ax.plot(times, temps, label="Temperature")
    ax.plot(times, humidity, label="Humidity")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend(loc="lower left")


def publish_data(client, temps):
    if not temps:
        return
    payload = "OFF"
    if temps[-1] > 28:
        payload = "ON"
    client.publish(topic_control, payload)
    print("Opublikowano: " + payload)


client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)
client.subscribe(topic)
print(f"Topic subscription '{ topic }' on broker { broker_address }:{ broker_port }")
client.loop_start()
ani = animation.FuncAnimation(fig, chart, interval=5000, save_count=50)
plt.ion()
plt.show(block=False)
try:
    while True:
        publish_data(client, temps)
        time.sleep(5)
except KeyboardInterrupt:
    print("Przerwanie programu przez użytkownika.")
finally:
    client.loop_stop()
    client.disconnect()