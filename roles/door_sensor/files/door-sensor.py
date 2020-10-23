#! /usr/bin/env python3

import time
import logging

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

LOCK_PIN = 8
MQTT_GATEWAY = "localhost"
MQTT_PORT = 1883

log = logging.getLogger("logger")
mqttClient = mqtt.Client("door-sensor")


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(LOCK_PIN, GPIO.BOTH, callback=status_callback)


def get_lock_status():
    return GPIO.input(LOCK_PIN)


def publish_lock_status():
    published_status = "ON" if get_lock_status() else "OFF"

    log.warning("publishing locked status: %s", published_status)

    mqttClient.connect(MQTT_GATEWAY, MQTT_PORT)
    mqttClient.publish("home/entrance/door/locked", published_status)


def status_callback(_channel):
    publish_lock_status()
    time.sleep(0.5)


def main():
    setup()

    while True:
        publish_lock_status()
        time.sleep(100)

    GPIO.cleanup()


if __name__ == "__main__":
    main()
