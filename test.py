#!/usr/bin/env python3
"""
    Test harness for dragino module - sends hello world out over LoRaWAN 5 times
    and adheres to a 1% duty cycle

    cache.json will be created if it doesn't exist
"""

# Make it possible to run the program on non-SBC machines.
import os
if "NOSBC" in os.environ:
    import mock_sbc
    mock_sbc.enable()
else:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)

import logging
from time import sleep
from dragino import Dragino

if "NOSBC" in os.environ:
    mock_sbc.monkeypatch_sx127x_post()

# add logfile
logLevel=logging.DEBUG
logging.basicConfig(filename="test.log", format='%(asctime)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s', level=logLevel)

# create a Dragino object and join to TTN
D = Dragino("dragino.toml", logging_level=logLevel)
D.join()

print("Waiting for JOIN ACCEPT")
while not D.registered():
    print(".",end="")
    sleep(2)
print("\nJoined")

for i in range(0, 5):
    D.send("Hello World")
    print("Sent Hello World message")
    while D.transmitting():
        sleep(0.1)
    sleep(99*D.lastAirTime()) # limit to 1% duty cycle
