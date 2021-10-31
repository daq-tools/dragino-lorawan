"""
Mock out all modules only installable on Raspberry Pi.

The idea behind this is to be able to run the Dragino LoRaWAN implementation
within a test harness.
"""
import sys
from unittest.mock import patch, MagicMock


def monkeypatch_rpi():
    try:
        import RPi.GPIO as GPIO
    except:
        import Mock.GPIO as GPIO
        sys.modules["RPi"] = MagicMock()
        sys.modules["RPi.GPIO"] = GPIO

    sys.modules["spidev"] = MagicMock()


def monkeypatch_gpsd():
    sys.modules["gpsd"] = MagicMock()


def monkeypatch_sx127x():
    sys.modules["dragino.SX127x.board_config"] = MagicMock()


def monkeypatch_sx127x_post():
    import dragino
    from dragino.SX127x.LoRa import LoRa as orig
    orig.get_freq = lambda x: 5.
    def set_mode(self, mode):
        self.mode = 0x80
    orig.set_mode = set_mode
    orig.get_agc_auto_on = lambda x: 1
    dragino.SX127x.LoRa.LoRa = orig


def enable():
    #monkeypatch_rpi()
    #monkeypatch_gpsd()
    monkeypatch_sx127x()
