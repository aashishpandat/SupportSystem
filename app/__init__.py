import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

from app.extensions import db

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.ticket_routes import ticket_bp
    app.register_blueprint(ticket_bp, url_prefix="/api")

    from app.models.ticket import Ticket

    with app.app_context():
        db.create_all()

        with db.engine.connect() as connection:
            connection.execute(db.text("SELECT 1"))

    print("MySQL database connected successfully!")
    print("Database tables created successfully!")

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({
            "success": False,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception("Unexpected server error")

        return jsonify({
            "success": False,
            "message": "An unexpected server error occurred"
        }), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return {
            "success": True,
            "message": "Support System API is running",
            "status": "healthy"
        }, 200

    return app