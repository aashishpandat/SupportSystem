# Support Ticket Management System

A RESTful backend API for managing customer support tickets, built with Flask and MySQL.

Developed as part of the ShadowFox Backend Developer task, this project focuses on clean architecture, input validation, database operations, and reliable API responses.

## Live Demo

**Health Check:**  
https://supportsystem-production-7af0.up.railway.app/api/health

**Get All Tickets:**  
https://supportsystem-production-7af0.up.railway.app/api/tickets

The deployed API can be tested using Postman or another HTTP client.

## Features

- Create and retrieve support tickets
- Retrieve an individual ticket by ID
- Update ticket details
- Change ticket status
- Delete tickets
- Validate required fields, email addresses, priorities, and statuses
- Handle invalid input, missing tickets, and database errors
- Automated unit and API tests using pytest

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** MySQL
- **ORM:** Flask-SQLAlchemy
- **Database Driver:** PyMySQL
- **Testing:** pytest
- **API Testing:** Postman
- **Deployment:** Railway

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check API health |
| POST | `/api/tickets` | Create a ticket |
| GET | `/api/tickets` | Retrieve all tickets |
| GET | `/api/tickets/<ticket_id>` | Retrieve a ticket by ID |
| PUT | `/api/tickets/<ticket_id>` | Update ticket details |
| PATCH | `/api/tickets/<ticket_id>/status` | Update ticket status |
| DELETE | `/api/tickets/<ticket_id>` | Delete a ticket |

### Ticket Fields

| Field | Description |
|---|---|
| `customer_name` | Customer's name |
| `email` | Customer's email address |
| `subject` | Ticket subject |
| `description` | Details of the issue |
| `priority` | `Low`, `Medium`, or `High` |
| `status` | `Open`, `In Progress`, or `Closed` |

New tickets default to `Medium` priority and `Open` status, unless configured otherwise by the application.

## Example Request

Create a ticket using `POST /api/tickets` with the following JSON body:

```json
{
  "customer_name": "Aashish",
  "email": "aashish@example.com",
  "subject": "Login issue",
  "description": "Unable to log in to my account",
  "priority": "High"
}
```

A successful request returns HTTP `201 Created`, along with the created ticket and a success message.

## Project Architecture

The application separates HTTP handling, validation, business logic, and database operations into dedicated layers.

```text
SupportSystem/
├── app/
│   ├── models/
│   │   └── ticket.py
│   ├── routes/
│   │   └── ticket_routes.py
│   ├── validation/
│   │   └── ticket_validator.py
│   ├── services/
│   │   └── ticket_service.py
│   ├── repositories/
│   │   └── ticket_repository.py
│   ├── extensions.py
│   └── __init__.py
├── tests/
│   ├── test_ticket_routes.py
│   ├── test_ticket_service.py
│   └── test_ticket_validator.py
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

### Layer Responsibilities

- **Routes / Controllers:** Handle HTTP requests and return JSON responses.
- **Validation:** Check request data and enforce allowed values.
- **Service:** Coordinate business logic and application operations.
- **Repository:** Handle database queries and persistence.
- **Models:** Define the ticket database structure.
- **Tests:** Verify validation, service behavior, and API endpoints.

## Getting Started

### Prerequisites

- Python 3.10 or later
- MySQL Server
- Git

### 1. Clone the repository

```bash
git clone https://github.com/aashishpandat/SupportSystem.git
cd SupportSystem
```

### 2. Create and activate a virtual environment

**Windows CMD:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the database connection settings expected by the application.

Do not commit `.env` or share database passwords publicly. Make sure MySQL is running and the configured database exists.

### 5. Run the application

```bash
python run.py
```

The local API will be available at:

`http://127.0.0.1:5000`

Health check:

`http://127.0.0.1:5000/api/health`

## Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The current test suite contains **13 passing tests**, covering ticket validation, service behavior, and API routes.

## API Testing with Postman

Import or create requests for the endpoints listed above. Test successful requests as well as invalid email addresses, missing fields, invalid priorities or statuses, and ticket IDs that do not exist.

## Author

**Aashish Jha**

- GitHub: https://github.com/aashishpandat
- LinkedIn: https://www.linkedin.com/in/aashish-jha/
