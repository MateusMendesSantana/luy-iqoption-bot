import random
import time
import json
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
print("login...")
I_want_money = IQ_Option("mateusmendessantana@hotmail.com", "zoom3.m.2009")
I_want_money.change_balance("REAL")
ACTIVES="EURUSD"
ACTION="call"
expirations_mode=1
force_buy= False
cost=1
optionID = 0
print("")
print("Buying option...")
print("Cost: ${}".format(cost))
optionID = I_want_money.buy(cost,ACTIVES,ACTION,expirations_mode,force_buy)
print(ACTIVES+" - History")
print("--------------------------------")
print("Option ID: {}".format(optionID))
time.sleep(0)
cost=cost+0.01