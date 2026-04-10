from config import *
from qweather import get_weather

def get_humidity_signal():
    h = get_weather()["humidity"]
    return h > 60, h
