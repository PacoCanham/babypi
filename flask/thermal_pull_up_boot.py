#!/usr/bin/python3
import RPi.GPIO as GPIO

GPIO_PIN_NUMBER=8
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("Enabled Thermal Probe")
