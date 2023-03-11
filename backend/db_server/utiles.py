from enum import Enum
from typing import Dict, Any

from flask import jsonify
from flask_mail import Mail, Message

SENDER_EMAIL = "bs5295@gmail.com"


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


def make_db_server_response(status_code: HttpStatus, message: str, data: Dict[Any, Any]):
    response = {
        'message': message,
        'data': data
    }
    return jsonify(response), status_code.value


def send_welcome_email():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Define email contents
    sender_email = SENDER_EMAIL
    receiver_email = 'bar_sela@gmail.com'
    password = 'bs52951998'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Welcome to our website!'
    body = 'Dear [Name],\n\nThank you for signing up for our website. We are thrilled to have you on board and hope you enjoy our services.\n\nBest regards,\n[Your Name]'
    message.attach(MIMEText(body, 'plain'))

    # Set up SMTP connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    # Send email
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
