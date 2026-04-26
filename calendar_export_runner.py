from pathlib import Path

from googleapiclient.discovery import build

from calendar_export import run_export
from google_calendar_auth import GoogleCalendarAuth

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = Path("token.json")
CLIENT_SECRETS_FILE = "client_secret.json"

def main():
    auth = GoogleCalendarAuth(TOKEN_FILE, CLIENT_SECRETS_FILE, SCOPES)
    creds = auth.get_credentials()
    service = build("calendar", "v3", credentials=creds)
    run_export(service, days_from_today=1)


if __name__ == "__main__":
    main()
