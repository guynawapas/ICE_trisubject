import os

import pyrebase

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

url=storage.child('yoyo.jpg').get_url(None)
print(url)