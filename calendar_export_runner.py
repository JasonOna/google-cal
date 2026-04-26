import sys
from pathlib import Path

from googleapiclient.discovery import build

from calendar_export import run_export_day
from google_calendar_auth import GoogleCalendarAuth

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = Path("token.json")
CLIENT_SECRETS_FILE = "client_secret.json"

def main():
    days_from_today = 1
    if len(sys.argv) > 1:
        try:
            days_from_today = int(sys.argv[1])
        except ValueError:
            print(f"Invalid days_from_today: {sys.argv[1]}", file=sys.stderr)
            sys.exit(1)

    auth = GoogleCalendarAuth(TOKEN_FILE, CLIENT_SECRETS_FILE, SCOPES)
    creds = auth.get_credentials()
    service = build("calendar", "v3", credentials=creds)
    run_export_day(service, days_from_today=days_from_today)


if __name__ == "__main__":
    main()
