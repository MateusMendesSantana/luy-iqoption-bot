import random
import time
import json
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime

print("login...")
api = IQ_Option("mateusmendessantana@hotmail.com", "zoom3.m.2009")
api.change_balance("PRACTICE")
profits = api.get_all_profit()
print(profits)