from flask import Blueprint, request, jsonify

from app.services.ticket_service import TicketService


ticket_bp = Blueprint("ticket_bp", __name__)


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

    ticket, error, status_code = TicketService.create_ticket(data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    return jsonify({
        "success": True,
        "message": "Ticket created successfully",
        "ticket": ticket_to_dict(ticket)
    }), status_code


@ticket_bp.route("/tickets", methods=["GET"])
def get_tickets():
    tickets, error, status_code = TicketService.get_all_tickets()

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    ticket_list = [ticket_to_dict(ticket) for ticket in tickets]

    return jsonify({
        "success": True,
        "count": len(ticket_list),
        "tickets": ticket_list
    }), status_code


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    ticket, error, status_code = TicketService.get_ticket(ticket_id)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    return jsonify({
        "success": True,
        "ticket": ticket_to_dict(ticket)
    }), status_code


@ticket_bp.route("/tickets/<int:ticket_id>/status", methods=["PATCH"])
def update_ticket_status(ticket_id):
    data = request.get_json()

    ticket, error, status_code = TicketService.update_ticket_status(
        ticket_id, data
    )

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    return jsonify({
        "success": True,
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.id,
        "status": ticket.status
    }), status_code


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):
    data = request.get_json()

    ticket, error, status_code = TicketService.update_ticket(
        ticket_id, data
    )

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    return jsonify({
        "success": True,
        "message": "Ticket updated successfully",
        "ticket": ticket_to_dict(ticket)
    }), status_code


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    deleted_ticket_id, error, status_code = TicketService.delete_ticket(
        ticket_id
    )

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), status_code

    return jsonify({
        "success": True,
        "message": "Ticket deleted successfully",
        "ticket_id": deleted_ticket_id
    }), status_code