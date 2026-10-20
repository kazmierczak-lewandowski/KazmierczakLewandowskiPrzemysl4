import RPi.GPIO as GPIO
import time
import random

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.output(19, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)

    leds = [19,18,13,12]
    random.seed()
    while True:
        if GPIO.input(17) == 0:
            print("SW1")
            randomLED = random.randrange(4)
            GPIO.output(leds[randomLED], GPIO.HIGH)
            time.sleep(0.5)
        if GPIO.input(4) == 0:
            print("SW2")
            randomNumberLEDs = random.randrange(1, 5)
            ledsNotSelected = leds.copy()
            for i in range(randomNumberLEDs):
                randomLED = random.randrange(4-i)
                GPIO.output(ledsNotSelected[randomLED], GPIO.HIGH)
                ledsNotSelected.remove(ledsNotSelected[randomLED])
            time.sleep(0.5)
        if GPIO.input(3) == 0:
            print("SW3")
            GPIO.output(19, GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            time.sleep(0.5)
        if GPIO.input(2) == 0:
            print("SW4")
            time.sleep(0.5)
            break
    GPIO.cleanup()
