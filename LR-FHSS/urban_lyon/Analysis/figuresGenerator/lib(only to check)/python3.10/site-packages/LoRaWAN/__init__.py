#__all__ = ['PhyPayload', 'MHDR']
from LoRaWAN.MHDR import *
from LoRaWAN.PhyPayload import PhyPayload

def new(nwkey = [], appkey = []):
    return PhyPayload(nwkey, appkey)
