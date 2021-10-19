import nfc
import time,os
import paho.mqtt.client as mqtt
clf = nfc.ContactlessFrontend('usb:001:005')
from binascii import hexlify
from nfc.clf import RemoteTarget
from dotenv import load_dotenv

load_dotenv()
client = mqtt.Client()
while(1):
    try:
        target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
        if(target is not None):
            client.connect(os.getenv('SERVER-IP'),1883)
            nfc_id = hexlify(target.sdd_res).decode()
            print(nfc_id)
            client.publish("nfc_id", nfc_id)
        else:
            print("no data")
            pass
    except:
        print('error')

    time.sleep(1)
