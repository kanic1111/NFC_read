# 讀取RFID或NFC卡片或設備上的標籤 並透過MQTT轉送給server
### 安裝必要套件

```shell=
sudo pip3 install -r requirement.txt
```

### 確認NFC儀器連接的位置
透過我們下載的nfcpy套件可以幫助我們查看是否有連接至NFC設備
```shell=
sudo python3 -m nfc
```
打完指令後在shell上可以看到自己連接的設備與連接的位址(之後要用)
![](https://i.imgur.com/dcyIriE.png)
由上圖可以看到我們連接的設備為ACS ACR122U 位址在usb:001:005
接下來就可透過python去讀取卡片資料
### 讀取卡片上id
```python=
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
        target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F')) #卡片可能有分種類 這邊就讀取所有卡片上的全部資料
        if(target is not None):
            client.connect(os.getenv('SERVER-IP'),1883)
            nfc_id = hexlify(target.sdd_res).decode() #透過target.sdd_res得出來的出來的資料會是byte形式的 須透過hexlify在解碼才能得到正確的id
            print(nfc_id)
            client.publish("nfc_id", nfc_id)
        else:
            print("no data")
            pass
    except:
        print('error')

    time.sleep(1)
```
