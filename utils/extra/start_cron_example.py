import requests


url = "https://example.com/cron/gd"

data = {"master_key": "enter your master key (without SHA256 encrypt)"}

response = requests.post(url, data=data, verify=False)