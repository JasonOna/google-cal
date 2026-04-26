from datetime import datetime, timedelta

import html2text

HTML_TO_MARKDOWN = html2text.HTML2Text()
HTML_TO_MARKDOWN.body_width = 0

def description_to_markdown(description):
    return HTML_TO_MARKDOWN.handle(description).strip()

# Fetch events from a day `days_from_today` days
# away from today in the local timezone.
def date_of_events(days_from_today: int):
    today = datetime.now().astimezone().replace(hour=0, minute=0, second=0, microsecond=0)
    start_day = today - timedelta(days=days_from_today)
    end_day = start_day + timedelta(days=1)
    return start_day, end_day

def get_events(service, start_day, end_day):
    return service.events().list(
        calendarId='primary',
        timeMin=start_day.isoformat(),
        timeMax=end_day.isoformat(),
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


def print_events(events, date_string):
    if not events:
        print(f'No events found for {date_string}.')
        return

    print(f'{date_string} events:')
    for event in events:
        print_event_details(event)


def run_export_day(service, days_from_today=1):
    start_day, end_day = date_of_events(days_from_today)
    
    events_result = get_events(service, start_day, end_day)
    events = events_result.get('items', [])
    print_events(events, start_day.isoformat())
