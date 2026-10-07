# Support Ticket Management System

A simple backend application for managing customer support tickets.

I built this project using Flask and MySQL as part of my ShadowFox Backend Developer task. The main focus was on creating REST APIs, connecting the application with a database, validating user input, and handling common API errors.

## What it can do

- Create a support ticket
- View all tickets
- View a ticket using its ID
- Update ticket status
- Update ticket details
- Delete a ticket
- Validate email, priority and status
- Handle invalid requests and missing data

## Technologies Used

- Python
- Flask
- MySQL
- Flask-SQLAlchemy
- PyMySQL
- Postman

## API Routes

| Method | Route | What it does |
|---|---|---|
| GET | `/api/health` | Checks if the API is running |
| POST | `/api/tickets` | Creates a ticket |
| GET | `/api/tickets` | Shows all tickets |
| GET | `/api/tickets/<id>` | Shows one ticket |
| PATCH | `/api/tickets/<id>/status` | Changes ticket status |
| PUT | `/api/tickets/<id>` | Updates ticket details |
| DELETE | `/api/tickets/<id>` | Deletes a ticket |

## Ticket Status

- Open
- In Progress
- Closed

## Priority

- Low
- Medium
- High

## Example

{
  "customer_name": "Aashish",
  "email": "aashish@example.com",
  "subject": "Login issue",
  "description": "Unable to login to my account",
  "priority": "High"
}

## Project Structure

SupportSystem/
│
├── app/
│   ├── models/
│   │   └── ticket.py
│   ├── routes/
│   │   └── ticket_routes.py
│   ├── extensions.py
│   └── __init__.py
│
├── .gitignore
├── run.py
└── README.md

## Testing

I tested the APIs using Postman, including normal requests as well as invalid email, priority, status and missing-field cases.

## Running the project

Install the required packages:

pip install -r requirements.txt

Set the database details in the `.env` file and then run:

python run.py

The API will be available at:

http://127.0.0.1:5000