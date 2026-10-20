import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)
    time.sleep(2)

    GPIO.output(19, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    time.sleep(2)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    time.sleep(2)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)
    time.sleep(2)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)
    time.sleep(2)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    time.sleep(2)

    GPIO.cleanup()