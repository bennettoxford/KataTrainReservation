import os
import signal
import subprocess
import sys
import time
import urllib.request
import json

import pytest


def test_reserve_seats():
    form_data = {"train_id": "express_2000", "seat_count": 4}
    data = urllib.parse.urlencode(form_data)

    req = urllib.request.Request("http://127.0.0.1:8083/reserve", bytes(data, encoding="ISO-8859-1"))
    response = urllib.request.urlopen(req).read().decode("ISO-8859-1")
    reservation = json.loads(response)

    assert reservation["train_id"] == "express_2000"
    assert len(reservation["seats"]) == 4
    assert reservation["seats"][0] == "1A"
    assert reservation["booking_reference"] == "75bcd15"


@pytest.fixture(scope="session", autouse=True)
def services():
    processes = []
    try:
        processes.append(start_service(["train_data_service/train_data_service.py"]))
        processes.append(start_service(["booking_reference_service/booking_reference_service.py"]))
        processes.append(start_service(["python/ticket_office.py"]))

        wait_for_service("http://127.0.0.1:8081/data_for_train/express_2000")
        wait_for_service("http://127.0.0.1:8082/booking_reference")
        wait_for_service("http://127.0.0.1:8083/reserve")

        yield
    finally:
        for p in processes:
            p.terminate()
            p.wait()


def wait_for_service(url, timeout=5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError(f"Service at {url} did not start in time")


def start_service(args):
    return subprocess.Popen([sys.executable] + args)
