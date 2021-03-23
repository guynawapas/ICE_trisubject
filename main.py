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

camera = PiCamera()
camera.rotation = 90

allpicslist = []

picture = ""

firebaseConfig = {
    "apiKey": "AIzaSyDl_cOyzvWLAq11mU-9IAq8d3X9ey2GBeM",
    "authDomain": "testpicupload.firebaseapp.com",
    "databaseURL": "https://testpicupload-default-rtdb.firebaseio.com",
    "projectId": "testpicupload",
    "storageBucket": "testpicupload.appspot.com",
    "messagingSenderId": "847787661172",
    "appId": "1:847787661172:web:4ed855f697939cdad97e21"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
#upload
#storage.child("yoyo.jpg").put("test1.jpg")

#Download
#storage.child("yoyo.jpg").download(filename="Download_name.jpg",path=os.path.basename(""))

#url=storage.child('yoyo.jpg').get_url(None)
#print(url)


while(True):
    
    #value = input("Enter 'c' to take a picture, Type \"stop\" to exit:\n")
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
        camera.start_preview()
        sleep(5)
        camera.capture(picture, quality=30) #quality range 0-100
        camera.stop_preview()
        allpicslist.append(str(x))
        #print(allpicslist)
        
        #url = "https://api.aiforthai.in.th/lpr-v2"
        url = "https://api.aiforthai.in.th/panyapradit-lpr"
        #payload = {'crop': '1', 'rotate': '1'}
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
            
            #upload picture to firebase
            path_firebase = "/images/"+"license"+str(x)+".jpeg"
            storage.child(path_firebase).put(picture)
            
            #get the url
            url=storage.child(path_firebase).get_url(None)
            print("access picture: "+url)
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






