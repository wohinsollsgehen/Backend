# import time
# import ttn
from classes.input.ttn import InputTTN

# TODO: each input in one thread / parallel
ttnInstance = InputTTN()
ttnInstance.fetch();