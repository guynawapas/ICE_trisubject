import numpy as np
import json
import matplotlib.pyplot as plot
import matplotlib.patches as patches
import requests



url = "https://api.aiforthai.in.th/panyapradit-lpr"
        #payload = {'crop': '1', 'rotate': '1'}
files = {'file': open("./images/license2021-02-20 17:52:24.090410.jpeg", 'rb')}
headers = {
    'Apikey': "9fyO2hLVgXRem15kSZ86XVOC2fgJwcqR",
}
        


response = requests.post(url, files=files, headers=headers)
if response.status_code == 204:
    print("..")
    
        

data = response.json()
    #temp = data[0]
print(data)
r_char = data['r_char']
r_digit = data['r_digit'].lstrip("0")
r_province = data['r_province']
print(r_char,r_digit,r_province)
