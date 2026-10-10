from app.validation.ticket_validator import TicketValidator


def valid_ticket_data():
    return {
        "customer_name": "Aashish",
        "email": "aashish@example.com",
        "subject": "Login issue",
        "description": "Unable to login to my account"
    }


def test_valid_ticket_data():
    data, error = TicketValidator.validate_ticket_data(
        valid_ticket_data()
    )

    assert error is None
    assert data["customer_name"] == "Aashish"
    assert data["priority"] == "Medium"


def test_missing_customer_name():
    payload = valid_ticket_data()
    payload["customer_name"] = " "

    data, error = TicketValidator.validate_ticket_data(payload)

    assert data is None
    assert error == "customer_name is required and must be valid text"


def test_invalid_email():
    payload = valid_ticket_data()
    payload["email"] = "invalid-email"

    data, error = TicketValidator.validate_ticket_data(payload)

    assert data is None
    assert error == "Please provide a valid email address"


def test_invalid_priority():
    payload = valid_ticket_data()
    payload["priority"] = "Urgent"

    data, error = TicketValidator.validate_ticket_data(payload)

    assert data is None
    assert error == "Priority must be Low, Medium, or High"


def test_valid_status():
    status, error = TicketValidator.validate_status({
        "status": "In Progress"
    })

    assert status == "In Progress"
    assert error is None


def test_invalid_status():
    status, error = TicketValidator.validate_status({
        "status": "Pending"
    })

    assert status is None
    assert error == "Status must be Open, In Progress, or Closed"