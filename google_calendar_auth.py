from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleCalendarAuth:
    def __init__(self, token_file, client_secrets_file, scopes):
        self.token_file = Path(token_file)
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes

    def get_credentials(self):
        creds = None

        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.scopes
                )
                creds = flow.run_local_server(port=0)

            self.token_file.write_text(creds.to_json())

        return creds
