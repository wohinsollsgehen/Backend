# import time
# import ttn
from classes.input.ttn import InputTTN

with InputTTN() as ttnInstance:
    ttnInstance.fetch();