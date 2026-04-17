import subprocess
import sys
import time

import pytest
import requests


def test_reserve_seats():
    response = requests.post("http://127.0.0.1:8083/reserve", data={
        "train_id": "express_2000",
        "seat_count": 4,
    })
    response.raise_for_status()
    reservation = response.json()

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
            requests.get(url, timeout=1)
            return
        except requests.ConnectionError:
            time.sleep(0.1)
    raise TimeoutError(f"Service at {url} did not start in time")


def start_service(args):
    return subprocess.Popen([sys.executable] + args)
