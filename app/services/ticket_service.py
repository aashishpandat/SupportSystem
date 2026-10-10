from app.validation.ticket_validator import TicketValidator
from app.repositories.ticket_repository import TicketRepository


class TicketService:

    @staticmethod
    def create_ticket(data):
        ticket_data, error = TicketValidator.validate_ticket_data(data)

        if error:
            return None, error, 400

        try:
            ticket = TicketRepository.create(ticket_data)
            return ticket, None, 201
        except Exception:
            return None, "Unable to create ticket due to a database error", 500

    @staticmethod
    def get_all_tickets():
        try:
            tickets = TicketRepository.get_all()
            return tickets, None, 200
        except Exception:
            return None, "Unable to retrieve tickets", 500

    @staticmethod
    def get_ticket(ticket_id):
        try:
            ticket = TicketRepository.get_by_id(ticket_id)

            if ticket is None:
                return None, "Ticket not found", 404

            return ticket, None, 200
        except Exception:
            return None, "Unable to retrieve ticket", 500
        
    @staticmethod
    def update_ticket(ticket_id, data):
        try:
            existing_ticket = TicketRepository.get_by_id(ticket_id)

            if existing_ticket is None:
                return None, "Ticket not found", 404

            ticket_data, error = TicketValidator.validate_ticket_data(
                data,
                current_priority=existing_ticket.priority
            )

            if error:
                return None, error, 400

            ticket = TicketRepository.update(existing_ticket, ticket_data)
            return ticket, None, 200

        except Exception:
            return None, "Unable to update ticket due to a database error", 500

    @staticmethod
    def update_ticket_status(ticket_id, data):
        status, error = TicketValidator.validate_status(data)

        if error:
            return None, error, 400

        try:
            ticket = TicketRepository.get_by_id(ticket_id)

            if ticket is None:
                return None, "Ticket not found", 404

            ticket = TicketRepository.update_status(ticket, status)
            return ticket, None, 200
        except Exception:
            return None, "Unable to update ticket status due to a database error", 500
    
   
    @staticmethod
    def delete_ticket(ticket_id):
        try:
            ticket = TicketRepository.get_by_id(ticket_id)

            if ticket is None:
                return None, "Ticket not found", 404

            TicketRepository.delete(ticket)
            return ticket_id, None, 200
        except Exception:
            return None, "Unable to delete ticket due to a database error", 500