from iqoptionapi.stable_api import IQ_Option
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
api = IQ_Option("mateusmendessantana@hotmail.com", "zoom3.m.2009")

api.start_candles_stream("EURUSD-OTC", 15, 100)

candles: list = api.get_realtime_candles("EURUSD-OTC", 100)
print(candles)

api.start_candles_stream("GBPUSD-OTC", 15, 100)

candles: list = api.get_realtime_candles("GBPUSD-OTC", 100)
print(candles)
