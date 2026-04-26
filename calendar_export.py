from datetime import datetime, timedelta
from pathlib import Path

import html2text
from googleapiclient.discovery import build

from google_calendar_auth import GoogleCalendarAuth

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = Path("token.json")
CLIENT_SECRETS_FILE = "client_secret.json"

creds = None
HTML_TO_MARKDOWN = html2text.HTML2Text()
HTML_TO_MARKDOWN.body_width = 0

def description_to_markdown(description):
    return HTML_TO_MARKDOWN.handle(description).strip()

auth = GoogleCalendarAuth(TOKEN_FILE, CLIENT_SECRETS_FILE, SCOPES)
creds = auth.get_credentials()

service = build("calendar", "v3", credentials=creds)

# Fetch events from yesterday in the local timezone.
today = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
friday = today - timedelta(days=2)

events_result = service.events().list(
    calendarId='primary',
    timeMin=friday.isoformat(),
    timeMax=yesterday.isoformat(),
    maxResults=50,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

def print_event_details(event):
    raw_start = event['start'].get('dateTime')
    raw_end = event['end'].get('dateTime')

    start = ''
    end = ''
    if raw_start:
      start = datetime.fromisoformat(raw_start.replace("Z", "+00:00")).astimezone().strftime("%-I:%M %p")
    if raw_end:
      end = datetime.fromisoformat(raw_end.replace("Z", "+00:00")).astimezone().strftime("%-I:%M %p")

    print(f"* {event.get('summary', '(no title)')} {start} {end}")

    if event.get('description'):
        markdown_description = description_to_markdown(event['description'])
        print(f"\t* Description:\n{markdown_description}")
    print()

if not events:
    print('No events found for yesterday.')
else:
    print('Yesterday\'s events:')
    for event in events:
        print_event_details(event)
