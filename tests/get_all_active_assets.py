import random
import time
import json
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime

print("login...")
api = IQ_Option("mateusmendessantana@hotmail.com", "zoom3.m.2009")
api.change_balance("PRACTICE")
init_info = api.get_all_init()
actives = init_info["result"]["binary"]["actives"]


def fun(code):
    return actives[str(code)]["enabled"] == True

assets_enablets_code = list(filter(fun, actives))
assets_enablets = list(map(lambda code: actives[code], assets_enablets_code))
print(assets_enablets)
