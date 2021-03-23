import os
import requests
import pyrebase
import config
import json
import datetime


firebase = pyrebase.initialize_app(config.firebaseConfig)
storage = firebase.storage()
#upload
#storage.child("yoyo.jpg").put("test1.jpg")

#Download
storage.child("yoyo.jpg").download(filename="Download_name.jpg",path=os.path.basename(""))

url=storage.child('yoyo.jpg').get_url(None)
#print("picture url: "+url)

post_url = "http://somchai09.trueddns.com:43322/carentry"
headers={'Content-type':"application/json"}

payload={"entry_picture":url,
"building":"Rutsart",
"floor":4,
"parking_platenum":"กก1234",
"parking_platecity":"กรุงเทพมหานคร",
"entry_date":"01-01-2021",
"entry_time":"10:30:02"}

payload_json = json.dumps(payload)
#x = requests.post(post_url,data=payload_json,headers=headers)


#print(x.json())
time = datetime.datetime.now()
d_m_y = str(time.day)+"-"+str(time.month)+"-"+str(time.year)
h_m_s = time.strftime("%X")
print(d_m_y,h_m_s)