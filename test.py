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
# storage.child("yoyo.jpg").download(filename="Download_name.jpg",path=os.path.basename(""))

# url=storage.child('yoyo.jpg').get_url(None)
#print("picture url: "+url)

post_url = "http://somchai09.trueddns.com:43322/carentry"
headers_={'Content-type':"application/json"}

payload={"entry_picture":"testing",
"building":"Rutsart",
"floor":4,
"parking_platenum":"กก1234",
"parking_platecity":"กรุงเทพมหานคร",
"entry_date":"01-01-2021",
"entry_time":"10:30:02"}


# time = datetime.datetime.now()
# d_m_y = str(time.day)+"-"+str(time.month)+"-"+str(time.year)
# h_m_s = time.strftime("%X")
# print(d_m_y,h_m_s)


# payload_json = json.dumps(payload)
#x = requests.post(post_url,data=payload_json,headers=headers)


#print(x.json())


picture = "D:/Chula/Code/ThaiAPI/images/1.jpeg"
url = "https://api.aiforthai.in.th/panyapradit-lpr"
files = {'file': open(picture, 'rb')}
headers = {
    'Apikey': "9fyO2hLVgXRem15kSZ86XVOC2fgJwcqR",
}

response = requests.post(url, files=files, headers=headers)
x= datetime.datetime.now()
#license plate is recognized

data = response.json()
print(data)
r_char = data['r_char']
r_digit = data['r_digit'].lstrip("0")
r_province = data['r_province']
#print(r_char,r_digit,r_province)
plate_num = r_char+r_digit

#upload picture to firebase
path_firebase = "/images/"+"license"+str("testcam4")+".jpeg"
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
response_database = requests.post(post_url,data=payload_json,headers=headers_)
print(response_database.json())
