import re


class TicketValidator:
    REQUIRED_FIELDS = [
        "customer_name",
        "email",
        "subject",
        "description"
    ]

    ALLOWED_PRIORITIES = ["Low", "Medium", "High"]
    ALLOWED_STATUSES = ["Open", "In Progress", "Closed"]

    @staticmethod
    def validate_ticket_data(data, current_priority="Medium"):
        if not isinstance(data, dict):
            return None, "Request body must contain a valid JSON object"

        cleaned_data = {}

        for field in TicketValidator.REQUIRED_FIELDS:
            value = data.get(field)

            if not isinstance(value, str) or not value.strip():
                return None, f"{field} is required and must be valid text"

            cleaned_data[field] = value.strip()

        email = cleaned_data["email"]
        email_pattern = r"^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$"

        if not re.match(email_pattern, email):
            return None, "Please provide a valid email address"

        priority = data.get("priority", current_priority)

        if (
            not isinstance(priority, str)
            or priority not in TicketValidator.ALLOWED_PRIORITIES
        ):
            return None, "Priority must be Low, Medium, or High"

        cleaned_data["priority"] = priority

        return cleaned_data, None

    @staticmethod
    def validate_status(data):
        if not isinstance(data, dict) or "status" not in data:
            return None, "Status is required"

        status = data["status"]

        if (
            not isinstance(status, str)
            or status not in TicketValidator.ALLOWED_STATUSES
        ):
            return None, "Status must be Open, In Progress, or Closed"

        return status, None