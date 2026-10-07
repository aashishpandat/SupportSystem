import re

from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models.ticket import Ticket


ticket_bp = Blueprint("ticket_bp", __name__)


def is_valid_email(email):
    pattern = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


# Convert ticket data into a clean JSON format
def ticket_to_dict(ticket):
    return {
        "id": ticket.id,
        "customer_name": ticket.customer_name,
        "email": ticket.email,
        "subject": ticket.subject,
        "description": ticket.description,
        "priority": ticket.priority,
        "status": ticket.status
    }


@ticket_bp.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Request body must contain a valid JSON object"
        }), 400

    required_fields = [
        "customer_name",
        "email",
        "subject",
        "description"
    ]

    for field in required_fields:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "success": False,
                "message": f"{field} is required and must be valid text"
            }), 400

    customer_name = data["customer_name"].strip()
    email = data["email"].strip()
    subject = data["subject"].strip()
    description = data["description"].strip()

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Please provide a valid email address"
        }), 400

    priority = data.get("priority", "Medium")

    if not isinstance(priority, str) or priority not in ["Low", "Medium", "High"]:
        return jsonify({
            "success": False,
            "message": "Priority must be Low, Medium, or High"
        }), 400

    ticket = Ticket(
        customer_name=customer_name,
        email=email,
        subject=subject,
        description=description,
        priority=priority
    )

    try:
        db.session.add(ticket)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to create ticket due to a database error"
        }), 500

    return jsonify({
        "success": True,
        "message": "Ticket created successfully",
        "ticket": ticket_to_dict(ticket)
    }), 201


@ticket_bp.route("/tickets", methods=["GET"])
def get_tickets():

    tickets = Ticket.query.all()

    ticket_list = [ticket_to_dict(ticket) for ticket in tickets]

    return jsonify({
        "success": True,
        "count": len(ticket_list),
        "tickets": ticket_list
    }), 200


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "success": False,
            "message": "Ticket not found"
        }), 404

    return jsonify({
        "success": True,
        "ticket": ticket_to_dict(ticket)
    }), 200


@ticket_bp.route("/tickets/<int:ticket_id>/status", methods=["PATCH"])
def update_ticket_status(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "success": False,
            "message": "Ticket not found"
        }), 404

    data = request.get_json()

    if not isinstance(data, dict) or "status" not in data:
        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    new_status = data["status"]

    if not isinstance(new_status, str) or new_status not in ["Open", "In Progress", "Closed"]:
        return jsonify({
            "success": False,
            "message": "Status must be Open, In Progress, or Closed"
        }), 400

    ticket.status = new_status

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to update ticket status due to a database error"
        }), 500

    return jsonify({
        "success": True,
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.id,
        "status": ticket.status
    }), 200


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "success": False,
            "message": "Ticket not found"
        }), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Request body must contain a valid JSON object"
        }), 400

    required_fields = [
        "customer_name",
        "email",
        "subject",
        "description"
    ]

    for field in required_fields:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "success": False,
                "message": f"{field} is required and must be valid text"
            }), 400

    customer_name = data["customer_name"].strip()
    email = data["email"].strip()
    subject = data["subject"].strip()
    description = data["description"].strip()

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "message": "Please provide a valid email address"
        }), 400

    priority = data.get("priority", ticket.priority)

    if not isinstance(priority, str) or priority not in ["Low", "Medium", "High"]:
        return jsonify({
            "success": False,
            "message": "Priority must be Low, Medium, or High"
        }), 400

    ticket.customer_name = customer_name
    ticket.email = email
    ticket.subject = subject
    ticket.description = description
    ticket.priority = priority

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to update ticket due to a database error"
        }), 500

    return jsonify({
        "success": True,
        "message": "Ticket updated successfully",
        "ticket": ticket_to_dict(ticket)
    }), 200


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "success": False,
            "message": "Ticket not found"
        }), 404

    try:
        db.session.delete(ticket)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to delete ticket due to a database error"
        }), 500

    return jsonify({
        "success": True,
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }), 200