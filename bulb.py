from yeelight import discover_bulbs
from yeelight import Bulb

bulb = None

def init_bulb():
    global bulb
    bulb = Bulb("192.168.0.124")


def switch_on():
    global bulb
    bulb.turn_on()


def switch_off():
    global bulb
    bulb.turn_off()
