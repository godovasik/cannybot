import json
import requests


with open("canny.json", "r") as file_json:
  print('opening json...')
  prompt = json.load(file_json)        
print(prompt)

p = {"prompt": prompt}
data = json.dumps(p).encode('utf-8')
requests.post("http://127.0.0.1:8188/prompt", data=prompt)