from ticket_office import TicketOffice


def test_reserve_seats():
    office = TicketOffice()
    result = office.reserve("express_2000", 4)
    assert result["train_id"] == "express_2000"
