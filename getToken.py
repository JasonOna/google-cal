from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = Path("token.json")
CLIENT_SECRETS_FILE = "client_secret.json"

creds = None

if TOKEN_FILE.exists():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            SCOPES
        )
        creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json())

service = build("calendar", "v3", credentials=creds)

# Fetch events from yesterday in the local timezone.
today = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)

events_result = service.events().list(
    calendarId='primary',
    timeMin=yesterday.isoformat(),
    timeMax=today.isoformat(),
    maxResults=50,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])


def print_event_details(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    attendees = ', '.join(
        attendee.get('email', 'unknown') for attendee in event.get('attendees', [])
    )

    print(f"Title: {event.get('summary', '(no title)')}")
    print(f"Start: {start}")
    print(f"End: {end}")
    print(f"Status: {event.get('status', 'unknown')}")

    if event.get('location'):
        print(f"Location: {event['location']}")
    if event.get('description'):
        print(f"Description: {event['description']}")
    if event.get('organizer', {}).get('email'):
        print(f"Organizer: {event['organizer']['email']}")
    if attendees:
        print(f"Attendees: {attendees}")
    if event.get('htmlLink'):
        print(f"Link: {event['htmlLink']}")
    print(f"Event ID: {event.get('id', 'unknown')}")
    print()

if not events:
    print('No events found for yesterday.')
else:
    print('Yesterday\'s events:')
    for event in events:
        print_event_details(event)