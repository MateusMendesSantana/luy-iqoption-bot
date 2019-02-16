import random
import time
import json
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime

email = "mateusmendessantana@hotmail.com"
password = "zoom3.m.2009"

print("login...")
I_want_money = IQ_Option(email, password)
I_want_money.change_balance("PRACTICE")


ACTIVES = "EURUSD-OTC"
ACTION = "put"
expirations_mode = 1
force_buy = False
cost = 1
optionID = 0


while True:
    print("")
    print("Buying option...")
    print("Cost: ${}".format(cost))
    optionID = I_want_money.buy(cost, ACTIVES, ACTION, expirations_mode, force_buy)
    time.sleep(5)
    print(ACTIVES+" - History")
    print("--------------------------------")
    print("Option ID: {}".format(optionID))
    time.sleep(65)
