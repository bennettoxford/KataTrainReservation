"""
You can get information about which seats each train has by using this service.
For test purposes, you can start a local service using this code. You can
assume the real service will behave the same way, but be available on a
different url.

You can use this service to get data for example about the train with id
"express_2000" like this:

    http://localhost:8081/data_for_train/express_2000

This will return a json document with information about the seats that this
train has. The document you get back will look for example like this:

    {"seats": {"1A": {"booking_reference": "", "seat_number": "1", "coach": "A"},
               "2A": {"booking_reference": "", "seat_number": "2", "coach": "A"}}}

Note I've left out all the extraneous details about where the train is going
to and from, at what time, whether there's a buffet car etc. All that's there
is which seats the train has, and if they are already booked. A seat is
available if the "booking_reference" field contains an empty string.

To reserve seats on a train, you'll need to make a POST request to this url:

    http://localhost:8081/reserve

and attach form data for which seats to reserve. There should be three fields:

    "train_id", "seats", "booking_reference"

The "seats" field should be a json encoded list of seat ids, for example:

    '["1A", "2A"]'

The other two fields are ordinary strings. Note the server will prevent you
from booking a seat that is already reserved with another booking reference.

The service has one additional method, that will remove all reservations on a
particular train. Use it with care:

    http://localhost:8081/reset/express_2000
"""

import json
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)


class TrainDataService:
    def __init__(self, json_data):
        self.trains = json.loads(json_data)

    def data_for_train(self, train_id):
        return self.trains.get(train_id)

    def reserve(self, train_id, seats, booking_reference):
        train = self.trains.get(train_id)
        for seat in seats:
            if seat not in train["seats"]:
                return "seat not found {0}".format(seat)
            existing_reservation = train["seats"][seat]["booking_reference"]
            if existing_reservation and existing_reservation != booking_reference:
                return "already booked with reference: {0}".format(existing_reservation)
        for seat in seats:
            train["seats"][seat]["booking_reference"] = booking_reference
        return self.data_for_train(train_id)

    def reset(self, train_id):
        train = self.trains.get(train_id)
        for seat_id, seat in train["seats"].items():
            seat["booking_reference"] = ""
        return self.data_for_train(train_id)


service = None


@app.route('/healthcheck')
def healthcheck():
    return ""


@app.route('/data_for_train/<train_id>')
def data_for_train(train_id):
    return jsonify(service.data_for_train(train_id))


@app.route('/reserve', methods=["POST"])
def reserve():
    train_id = request.form["train_id"]
    seats = json.loads(request.form["seats"])
    booking_reference = request.form["booking_reference"]
    return jsonify(service.reserve(train_id, seats, booking_reference))


@app.route('/reset/<train_id>')
def reset(train_id):
    return jsonify(service.reset(train_id))


if __name__ == "__main__":
    import sys

    if "-help" in sys.argv or "--help" in sys.argv or "-h" in sys.argv:
        print("""
Use this program to start a train data service:

    python {0}

It will start a service on:

    http://localhost:8081/data_for_train

You can pass on the command line the name of the json file to use as a data
source. It defaults to looking for "trains.json" in the current working
directory.

    python {0} trains.json
""".format(sys.argv[0]))
    else:
        import logging
        logging.getLogger("werkzeug").setLevel(logging.WARNING)
        trains_data_file = sys.argv[1] if sys.argv[1:] else Path(__file__).parent / "trains.json"
        with open(trains_data_file) as f:
            service = TrainDataService(f.read())
        app.run(port=8081)
