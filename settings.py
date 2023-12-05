# TYPE WALLET MODE
TYPE_WALLET = "argent"  # argent/braavos

# RANDOM WALLETS MODE
RANDOM_WALLET = True  # True/False

# removing a wallet from the list after the job is done
REMOVE_WALLET = False

SLEEP_FROM = 60
SLEEP_TO = 80

QUANTITY_THREADS = 1

THREAD_SLEEP_FROM = 150
THREAD_SLEEP_TO = 450

# GWEI CONTROL MODE
CHECK_GWEI = False
MAX_GWEI = 50

# Рандомизация гвея. Если включен режим, то максимальный гвей будет выбираться из диапазона
RANDOMIZE_GWEI = False  # if True, max Gwei will be randomized for each wallet for each transaction
MAX_GWEI_RANGE = [24, 27]

GAS_SLEEP_FROM = 500
GAS_SLEEP_TO = 700
# RETRY MODE
RETRY_COUNT = 3

# CAIRO VERSION CONTROL
CAIRO_VERSION = 1

FEE_MULTIPLIER = 1.2
