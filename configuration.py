USERNAME = 'mateusmendessantana@hotmail.com'
PASSWORD = 'V8DRLuReSanpGur'
MODE = 'PRACTICE' # REAL PRACTICE

TIME_RECONNECT = 10 #seconds

# size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
OPERATION_TIME = 60
OPERATION_MONEY = 1
# OPERATION_MONEY = .03 # 0-1 (0-100%), operar com quantos porcento da banca por operação?
OPERATION_WHEN_PROFIT = .5 # 0-1 (0-100%), operar ativos que estão com que porcentagem de ganho?
OPERATION_WHEN_WIN = .8 # 0-1 (0-100%), operar com quantos porcento de chance de ganhar?

MAX_BOTS = 8

CANDLE_SIZE = 60 #seconds
MAX_CANDLES = int(15 * 60 / CANDLE_SIZE)


SHORT_CANDLE = .3 # %, considerar todas as velas com o corpo n% abaixo da media, velas curtas
LONG_CANDLE = 1.2 # %, considerar todas as velas com o corpo maior que n% da media, velas longas
