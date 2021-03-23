import numpy as np
import json
import requests

from picamera import PiCamera
from time import sleep
import datetime
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)

import os
import pyrebase
import config
import json

camera = PiCamera()
camera.rotation = 90

allpicslist = []

picture = ""


firebase = pyrebase.initialize_app(config.firebaseConfig)
storage = firebase.storage()
#upload
#storage.child("yoyo.jpg").put("test1.jpg")

#Download
#storage.child("yoyo.jpg").download(filename="Download_name.jpg",path=os.path.basename(""))

#url=storage.child('yoyo.jpg').get_url(None)
#print(url)

post_url = "http://somchai09.trueddns.com:43322/carentry"
db_headers={'Content-type':"application/json"}

payload={"entry_picture":"",
"building":"",
"floor":4,
"parking_platenum":"",
"parking_platecity":"",
"entry_date":"0",
"entry_time":""}


while(True):
    
    value = ""
    i=GPIO.input(8)
    if i==1:               #When output from motion sensor is HIGH
        print("License plate detecting on process",i)
        value="c"
    if(value == "stop"):
        exit()
    
    if(value == "c"):
        x = datetime.datetime.now()
        picture = "/home/pi/Desktop/thaiAPI/images/license"+str(x)+".jpeg"
        print('smile!')
        #camera.start_preview()
        #sleep(5)
        camera.capture(picture, quality=30) #quality range 0-100
        #camera.stop_preview()
        allpicslist.append(str(x))
        #print(allpicslist)
        
        
        url = "https://api.aiforthai.in.th/panyapradit-lpr"
        files = {'file': open(picture, 'rb')}
        headers = {
            'Apikey': "9fyO2hLVgXRem15kSZ86XVOC2fgJwcqR",
        }

        response = requests.post(url, files=files, headers=headers)
        if response.status_code == 204:
            print("..")
            continue
        
        try:#license plate is recognized
            data = response.json()
            #print(data)
            r_char = data['r_char']
            r_digit = data['r_digit'].lstrip("0")
            r_province = data['r_province']
            print(r_char,r_digit,r_province)
            plate_num = r_char+r_digit
            
            #upload picture to firebase
            path_firebase = "/images/"+"license"+str(x)+".jpeg"
            storage.child(path_firebase).put(picture)
            
            #get the url
            url=storage.child(path_firebase).get_url(None)
            print("access picture: "+url)
            
            #format day month year hour minutes and seconds
            d_m_y = str(x.day)+"-"+str(x.month)+"-"+str(x.year)
            h_m_s = x.strftime("%X")
            
            #change payload value
            payload["parking_platenum"]= plate_num
            payload["parking_platecity"] = r_province
            payload["entry_date"] = d_m_y
            payload["entry_time"] = h_m_s
            
            payload_json = json.dumps(payload)
            response_database = requests.post(post_url,data=payload_json,headers=db_headers)
            print(response_database.json())
            time.sleep(10)
            
        except:#license plate is not recognizable
            print("can't recognize license plate")
            
            #test file upload----------------------------------------
            
            #path_firebase = "/images/"+"license"+str(x)+".jpeg"
            #storage.child(path_firebase).put(picture)
            
            #get the url
            #url=storage.child(path_firebase).get_url(None)
            #print("access picture: "+url)
            
            #--------------------------------------------------------
            continue
        
        
        
        
    else:#detect no motion
        print("No car detected")
        time.sleep(2)






