import requests
import os

url = 'https://rustambek2003.pythonanywhere.com/webhook'

Token = '5766174948:AAERI4lwWYzIfSPaLDBE9gWugxMpNAMgmVE'

payload = {
    "url":url
}

r = requests.get(f"https://api.telegram.org/bot{Token}/setWebhook", params=payload)
r = requests.get(f"https://api.telegram.org/bot{Token}/GetWebhookInfo", params=payload)



print(r.json())