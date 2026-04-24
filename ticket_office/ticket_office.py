from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


class TicketOffice:
    def reserve(self, train_id, seat_count):
        response = requests.get(f"http://localhost:8081/data_for_train/{train_id}")
        booking_ref_response = requests.get("http://localhost:8082/booking_reference")
        seats = response.json()

        seat_numbers = list(seats["seats"].keys())[:seat_count]
        if len(seat_numbers) < seat_count:
            seat_numbers = []

        return {"train_id":train_id, "seats":seat_numbers, "booking_reference": booking_ref_response.text}


service = None


@app.route('/healthcheck')
def healthcheck():
    return ""


@app.route('/reserve', methods=["POST"])
def reserve():
    train_id = request.form["train_id"]
    seat_count = int(request.form["seat_count"])
    return jsonify(service.reserve(train_id, seat_count))


if __name__ == "__main__":
    service = TicketOffice()
    app.run(port=8083, debug=True)
