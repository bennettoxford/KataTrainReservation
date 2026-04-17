import requests

url = "http://127.0.0.1:8082"

response = requests.get(url + "/booking_reference")
response.raise_for_status()
print("got booking reference:", response.text)
