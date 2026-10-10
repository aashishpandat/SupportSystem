import pytest
from unittest.mock import patch, MagicMock

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["success"] is True
    assert response.get_json()["status"] == "healthy"


@patch("app.services.ticket_service.TicketRepository.create")
def test_create_ticket(mock_create, client):
    mock_ticket = MagicMock()
    mock_ticket.id = 1
    mock_ticket.customer_name = "Aashish"
    mock_ticket.email = "aashish@example.com"
    mock_ticket.subject = "Login issue"
    mock_ticket.description = "Unable to login"
    mock_ticket.priority = "Medium"
    mock_ticket.status = "Open"

    mock_create.return_value = mock_ticket

    response = client.post(
        "/api/tickets",
        json={
            "customer_name": "Aashish",
            "email": "aashish@example.com",
            "subject": "Login issue",
            "description": "Unable to login"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["success"] is True
    assert response.get_json()["ticket"]["id"] == 1


def test_create_ticket_invalid_email(client):
    response = client.post(
        "/api/tickets",
        json={
            "customer_name": "Aashish",
            "email": "invalid-email",
            "subject": "Login issue",
            "description": "Unable to login"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_ticket_not_found(client):
    with patch(
        "app.services.ticket_service.TicketRepository.get_by_id",
        return_value=None
    ):
        response = client.get("/api/tickets/999999")

    assert response.status_code == 404
    assert response.get_json()["message"] == "Ticket not found"