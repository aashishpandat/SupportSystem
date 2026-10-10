from app.extensions import db
from app.models.ticket import Ticket


class TicketRepository:

    @staticmethod
    def create(ticket_data):
        ticket = Ticket(**ticket_data)

        try:
            db.session.add(ticket)
            db.session.commit()
            return ticket
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_all():
        return Ticket.query.order_by(Ticket.id.asc()).all()

    @staticmethod
    def get_by_id(ticket_id):
        return db.session.get(Ticket, ticket_id)

    @staticmethod
    def update(ticket, updated_data):
        try:
            for field, value in updated_data.items():
                setattr(ticket, field, value)

            db.session.commit()
            return ticket
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_status(ticket, status):
        try:
            ticket.status = status
            db.session.commit()
            return ticket
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete(ticket):
        try:
            db.session.delete(ticket)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise