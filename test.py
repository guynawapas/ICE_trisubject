import os

import pyrebase
import config

firebase = pyrebase.initialize_app(config.firebaseConfig)
storage = firebase.storage()
#upload
#storage.child("yoyo.jpg").put("test1.jpg")

#Download
#storage.child("yoyo.jpg").download(filename="Download_name.jpg",path=os.path.basename(""))

url=storage.child('yoyo.jpg').get_url(None)
print(url)