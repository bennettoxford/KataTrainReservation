from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


class TicketOffice:
    def reserve(self, train_id, seat_count):
        response = requests.get("http://localhost:8081/data_for_train/express_2000")
        seats = response.json()

        seat_numbers = list(seats["seats"].keys())[:seat_count]
        if len(seat_numbers) < seat_count:
            seat_numbers = []

        return {"train_id":train_id, "seats":seat_numbers}


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
