# Google Calendar Export

This repository exports Google Calendar events to plain-text files under `outputs/`. The main runner fetches one day at a time, converts any HTML description content to Markdown, and prints the result to stdout. The shell wrapper can backfill missing daily exports.

## What it does

- Authenticates with Google Calendar using OAuth.
- Reads events from the primary calendar.
- Exports one day per run to a text file if you redirect stdout.
- Converts event descriptions from HTML to Markdown.
- Keeps a cached OAuth token in `token.json` after the first login.

## Files

- `calendar_export_runner.py`: Python entry point for a single export run.
- `calendar_export.py`: Event fetching and formatting logic.
- `google_calendar_auth.py`: OAuth token handling and refresh flow.
- `run.sh`: Creates a virtual environment if needed, installs dependencies, and runs Python.
- `nightly_export.sh`: Backfills daily exports into `outputs/`.
- `outputs/`: Generated export files named by date, such as `2026-04-25.txt`.

## Requirements

- Python 3
- A Google Cloud OAuth client secret file named `client_secret.json`
- A writable `token.json` file for the cached OAuth token

Install dependencies with:

```bash
./run.sh -m pip install -r requirements.txt
```

## Setup

1. Create an OAuth client in Google Cloud for a desktop app.
2. Download the credentials JSON and save it as `client_secret.json` in the repo root.
3. Run the export once to open the browser-based consent flow.
4. After consent, the app writes `token.json` and reuses it on later runs.

## Usage

Run the default export for yesterday:

```bash
./run.sh calendar_export_runner.py
```

Export a different day by passing the number of days back from today:

```bash
./run.sh calendar_export_runner.py 2
```

Redirect output into a dated file:

```bash
./run.sh calendar_export_runner.py 1 > outputs/2026-04-25.txt
```

## Backfilling exports

The `nightly_export.sh` script checks the newest file in `outputs/` and fills in any missing days up to yesterday. It is designed to be run on macOS because it uses `date -j` and `date -v`.

```bash
./nightly_export.sh
```

## Notes

- Event times are printed in the local timezone.
- The runner looks at the primary calendar only.
- If there are no events for a day, the script prints a short "No events found" message.
- `outputs/` is generated data and can be recreated at any time by rerunning the exporter.

## NEXT STEPS

- Update `Details` parsing to handle multiple format types.
  - Google Calendar has various formats (ex: markdown, html, plain txt) for this field due to various calendar programs
  - I'll need to find a way to consistently parse this field to markdown no mater what format is used
