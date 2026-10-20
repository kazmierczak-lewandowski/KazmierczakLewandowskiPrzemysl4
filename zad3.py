import RPi.GPIO as GPIO
import time
import random

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    random.seed()

    leds = [19, 18, 13, 12]
    for led in leds:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)

    buttons = [17, 4, 3, 2]
    for button in buttons:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    reaction_time = []

    for j in range(10):
        random_sleep = random.randrange(5, 20)/10
        selected_led = random.randrange(4)
        time.sleep(random_sleep)
        GPIO.output(leds[selected_led], GPIO.HIGH)
        nonePressed = True
        correct = False
        start = time.time()
        while nonePressed:
            for button in buttons:
                if GPIO.input(button) == 0:
                    if button == buttons[selected_led]:
                        correct = True
                        reaction_time.append(time.time()-start)
                    nonePressed = False
                    break
        if(not correct):
            for led in leds:
                GPIO.output(led, GPIO.HIGH)
            break
        for led in leds:
            GPIO.output(led, GPIO.LOW)

    print("Best time: " + str(min(reaction_time)))
    avg = sum(reaction_time) / len(reaction_time)
    print("Average time: " + str(avg))
    GPIO.cleanup()
        
            