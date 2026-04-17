"""This module uses Flask to expose a TrainDataService to http requests"""

from flask import Flask, request
from train_data_service import TrainDataService


def start(trains_data):
    service = TrainDataService(trains_data)
    app = Flask(__name__)

    @app.route('/data_for_train/<train_id>')
    def data_for_train(train_id):
        return service.data_for_train(train_id)

    @app.route('/reserve', methods=["POST"])
    def reserve():
        train_id = request.form["train_id"]
        seat_ids = request.form["seats"]
        booking_reference = request.form["booking_reference"]
        return service.reserve(train_id, seat_ids, booking_reference)

    @app.route('/reset/<train_id>')
    def reset(train_id):
        return service.reset(train_id)

    app.run(port=8081)
