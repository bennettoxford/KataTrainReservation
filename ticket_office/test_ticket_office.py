from ticket_office import TicketOffice
import responses


def populate_train_data_service(count=None, numbers=None, train_id="express_2000"):
    assert not (count and numbers)
    if not numbers:
        if not count:
            count = 100
        numbers = [str(s) for s in range(count)]
    
    seat_data = {}
    for n in numbers:
        seat_data[n] = {}

    return responses.get(f"http://localhost:8081/data_for_train/{train_id}", json={"seats": seat_data})

@responses.activate
def test_reserve_seats_on_correct_train():
    populate_train_data_service(train_id="slow_2000")

    office = TicketOffice()
    result = office.reserve("slow_2000", 4)
    assert result["train_id"] == "slow_2000"

@responses.activate
def test_reserve_correct_number_of_seats_when_enough_seats_are_available():
    populate_train_data_service(count=10)

    office = TicketOffice()
    result = office.reserve("express_2000", 4)
    assert len(result["seats"]) == 4

@responses.activate
def test_reserves_no_seats_when_not_enough_seats():
    populate_train_data_service(count=2)

    office = TicketOffice()
    result = office.reserve("express_2000", 4)
    assert result['seats'] == []

@responses.activate
def test_check_seats_are_from_data_service():
    populate_train_data_service(numbers=["1A", "2A"])

    office = TicketOffice()
    result = office.reserve("express_2000", 2)

    assert set(result["seats"]) == {"1A","2A"}

@responses.activate
def test_correct_train_id_passed_to_other_service():
    populate_train_data_service(train_id="slow_2000")
    office = TicketOffice()
    office.reserve("slow_2000", 4)
    