"""
You can get a unique booking reference using this service. For test purposes,
you can start a local service using this code. You can assume the real service
will behave the same way, but be available on a different url.

You can use this service to get a unique booking reference. Make a GET request to:

    http://localhost:8082/booking_reference

This will return a string that looks a bit like this:

    75bcd15
"""

import itertools

from flask import Flask

app = Flask(__name__)


class BookingReferenceService:
    def __init__(self, starting_point):
        self.counter = itertools.count(starting_point)

    def booking_reference(self):
        next_number = next(self.counter)
        return str(hex(next_number))[2:]


service = None


@app.route('/booking_reference')
def booking_reference():
    return service.booking_reference()


if __name__ == "__main__":
    import sys

    if "-help" in sys.argv or "--help" in sys.argv or "-h" in sys.argv:
        print("""
Use this program to start a booking reference service:

    python {0}

The service will start on this url:

    http://localhost:8082/booking_reference

If you have to restart the service, you can continue counting from the
previous reference by passing it on the command line:

    python {0} 75bcd15
""".format(sys.argv[0]))
    else:
        starting_point = int(sys.argv[1], 16) + 1 if sys.argv[1:] else 123456789
        service = BookingReferenceService(starting_point)
        app.run(port=8082)
