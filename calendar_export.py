from datetime import datetime, timedelta

import html2text

HTML_TO_MARKDOWN = html2text.HTML2Text()
HTML_TO_MARKDOWN.body_width = 0

def description_to_markdown(description):
    return HTML_TO_MARKDOWN.handle(description).strip()


def get_events(service, days_from_today: int):
    # Fetch events from a window ending today in the local timezone.
    today = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    start_day = today - timedelta(days=days_from_today)

    return service.events().list(
        calendarId='primary',
        timeMin=start_day.isoformat(),
        timeMax=today.isoformat(),
        maxResults=50,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

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


def print_events(events):
    if not events:
        print('No events found for yesterday.')
        return

    print('Previous events:')
    for event in events:
        print_event_details(event)


def run_export(service, days_from_today=1):
    events_result = get_events(service, days_from_today)
    events = events_result.get('items', [])
    print_events(events)
