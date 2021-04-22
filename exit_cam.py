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


#camera config
CAMERA_FLOOR = '1'
CAMERA_LOCATION = 'Political Science'


camera = PiCamera()
camera.rotation = 90

picture = ""

firebase = pyrebase.initialize_app(config.firebaseConfig)
storage = firebase.storage()

server = {'post_url': "http://somchai09.trueddns.com:43322/carexit",
          'db_headers' : {'Content-type':"application/json"},
          'payload' : {"exit_picture":"",
                        "parking_platenum":"",
                        "parking_platecity":"",
                        "exit_datetime":"",
                        }
}

def capture():
    x = datetime.datetime.now()
    picture = "/home/pi/Desktop/thaiAPI/images/license"+str(x)+".jpeg"
    print('capturing')
    
    camera.capture(picture, quality=30) #quality range 0-100
    
    #test picture
    picture = "/home/pi/Desktop/thaiAPI/images/license2021-02-20 17:54:03.203731.jpeg"
    
    
    #license plate recognition API
    url = "https://api.aiforthai.in.th/panyapradit-lpr"
    files = {'file': open(picture, 'rb')}
    headers = {
        'Apikey': "9fyO2hLVgXRem15kSZ86XVOC2fgJwcqR",
    }

    response = requests.post(url, files=files, headers=headers)
    print(response)
    if response.status_code == 204:
        print("..")
        capture()
        return
    
    try:#license plate is recognized
        data = response.json()
        #print(data)
        r_char = data['r_char']
        if r_char[0] == '/':
            r_char = r_char[1:]
        r_digit = data['r_digit'].lstrip("0")
        r_province = data['r_province']
        print(r_char,r_digit,r_province)
        plate_num = r_char+r_digit
        
        
        
        #upload picture to firebase
        path_firebase = "/images/exit/"+"license"+str(x)+".jpeg"
        storage.child(path_firebase).put(picture)
        
        #get the url
        pic_url=storage.child(path_firebase).get_url(None)
        print("access picture: "+pic_url)
        
        
        #change payload value
        server['payload']['entry_picture'] = pic_url
        server['payload']["parking_platenum"]= plate_num
        server['payload']["parking_platecity"] = r_province
        server['payload']["exit_datetime"] = str(x.strftime("%Y-%m-%d %H:%M:%S"))
  
        
        payload_json = json.dumps(server['payload'])
        print(payload_json)
        response_database = requests.post(server['post_url'],data=payload_json,headers=server['db_headers'])
        print(response_database.json())
        time.sleep(10)
        
    except:#license plate is not recognizable
        print("can't recognize license plate")
        #capture()

while(True):
    
    value = ""
    i=GPIO.input(8)
    if i==1:               #When output from motion sensor is HIGH
        print("License plate detecting on process",i)
        value="c"
    if(value == "stop"):
        exit()
    
    if(value == "c"):
        capture()
        
    else:#detect no motion
        print("No car detected")
        time.sleep(2)





