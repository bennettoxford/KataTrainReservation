import urllib.request
import json

url = "http://127.0.0.1:8083"


def test_reserve_seats():
    form_data = {"train_id": "express_2000", "seat_count": 4}
    data = urllib.parse.urlencode(form_data)

    req = urllib.request.Request(url + "/reserve", bytes(data, encoding="ISO-8859-1"))
    response = urllib.request.urlopen(req).read().decode("ISO-8859-1")
    reservation = json.loads(response)

    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"][0] == "1A"
    assert reservation["booking_reference"] == "75bcd15"
