from __future__ import print_function
import base64
from logger_client import logger
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

SUBJECT = "Welcome To WiFix"


class EmailClient:
    def __init__(self):
        try:
            creds = None

            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    credentials_path = (
                        "/wifix/backend/db_server/welcome_email/credentials.json"
                    )
                    if not os.path.exists(credentials_path):
                        credentials_path = (
                            "backend/db_server/welcome_email/credentials.json"
                        )

                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path,
                        SCOPES,
                    )
                    creds = flow.run_local_server(port=0)

                with open("token.json", "w") as token:
                    token.write(creds.to_json())

            self.service = build("gmail", "v1", credentials=creds)
        except HttpError as error:
            logger.error(f"An error occurred: {error}")

        file_path = "/wifix/backend/db_server/welcome_email/welcome_email_template.html"
        if not os.path.exists(file_path):
            file_path = "welcome_email/welcome_email_template.html"

        with open(file_path, "r") as file:
            self.html_body = file.read()

    def send_email(self, to: str):
        message = MIMEMultipart()
        text = MIMEText(self.html_body, "html")
        message.attach(text)

        message["to"] = to
        message["subject"] = SUBJECT

        create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

        send_message = (
            self.service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        logger.info(f'sent welcome email to {to} Message Id: {send_message["id"]}')
