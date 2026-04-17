from flask import Flask, jsonify, request

app = Flask(__name__)


class TicketOffice:
    def reserve(self, train_id, seat_count):
        return {}


service = None


@app.route('/healthcheck')
def healthcheck():
    return ""


@app.route('/reserve', methods=["POST"])
def reserve():
    train_id = request.form["train_id"]
    seat_count = request.form["seat_count"]
    return jsonify(service.reserve(train_id, seat_count))


if __name__ == "__main__":
    import logging
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    service = TicketOffice()
    app.run(port=8083)
