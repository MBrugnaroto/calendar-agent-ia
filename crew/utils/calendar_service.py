import os

from dataclasses import dataclass, field

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


@dataclass
class Calendar():
    creds: str = field(default=None, init=False)
    token_path: str = field(
        default="/home/brugnaroto/Workspace/scripts-repository/agents/calendar-agent-ia/credentials/token.json",
        init=False
    )
    credentials_path: str = field(
        default="/home/brugnaroto/Workspace/scripts-repository/agents/calendar-agent-ia/credentials/credentials.json",
        init=False
    )
    service: build = field(default=None, init=False)

    def __post_init__(self):
        self.__get_credentials()
        self.__get_service()

    def __get_credentials(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

    def __get_service(self):
        self.service = build("calendar", "v3", credentials=self.creds)

    def get_calendar_timezone(self):
        try:
            timezone_config = self.service.settings().get(setting='timezone').execute()
            return timezone_config.get('value', 'America/Sao_Paulo')
        except HttpError as error:
            raise HttpError(f"An error occurred: {error}")
