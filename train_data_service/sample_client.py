import json
import requests

url = "http://127.0.0.1:8081"

# check for free seats on the train "express_2000"
response = requests.get(url + "/data_for_train/express_2000")
print("original reservation situation:", response.text)

# book a seat
response = requests.post(url + "/reserve", data={
    "train_id": "express_2000",
    "seats": json.dumps(["1A"]),
    "booking_reference": "01234567",
})
print("situation after reservation:", response.text)

# reserve the seat again and it is not updated
response = requests.post(url + "/reserve", data={
    "train_id": "express_2000",
    "seats": json.dumps(["1A"]),
    "booking_reference": "new_reference",
})
print("reservation should have failed:", response.text)

# remove all seat reservations for train express_2000
response = requests.get(url + "/reset/express_2000")
print("reservations are all removed:", response.text)
