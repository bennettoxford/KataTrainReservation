
class TicketOffice(object):

    def reserve(self, train_id, seat_count):
        # TODO: write this code!
        pass

if __name__ == "__main__":
    """Deploy this class as a web service using Flask"""
    from flask import Flask, request

    app = Flask(__name__)
    office = TicketOffice()

    @app.route('/reserve', methods=["POST"])
    def reserve():
        train_id = request.form["train_id"]
        seat_count = request.form["seat_count"]
        return office.reserve(train_id, seat_count)

    app.run(port=8083)
