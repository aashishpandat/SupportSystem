from unittest.mock import patch, MagicMock

from app.services.ticket_service import TicketService


def valid_ticket_data():
    return {
        "customer_name": "Aashish",
        "email": "aashish@example.com",
        "subject": "Login issue",
        "description": "Unable to login to my account"
    }


@patch("app.services.ticket_service.TicketRepository.create")
def test_create_ticket_success(mock_create):
    mock_ticket = MagicMock()
    mock_ticket.id = 1
    mock_create.return_value = mock_ticket

    ticket, error, status_code = TicketService.create_ticket(
        valid_ticket_data()
    )

    assert ticket is mock_ticket
    assert error is None
    assert status_code == 201
    mock_create.assert_called_once()


@patch("app.services.ticket_service.TicketRepository.create")
def test_create_ticket_invalid_data(mock_create):
    data = valid_ticket_data()
    data["email"] = "invalid-email"

    ticket, error, status_code = TicketService.create_ticket(data)

    assert ticket is None
    assert error == "Please provide a valid email address"
    assert status_code == 400
    mock_create.assert_not_called()


@patch("app.services.ticket_service.TicketRepository.get_by_id")
def test_get_ticket_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None

    ticket, error, status_code = TicketService.get_ticket(999)

    assert ticket is None
    assert error == "Ticket not found"
    assert status_code == 404