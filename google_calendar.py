import os
import datetime
import pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from get_date import get_and_validate_date

load_dotenv("./creds/.env")
MY_EMAIL = os.getenv('MY_EMAIL')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = './creds/creds.json'


def logger(info):
    line = '*' * 50
    print(f"{line}\n{info}\n{line}")


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def get_info_about_confirmed_events(events):
    approved_events = []
    for event in events:
        if event["status"] == "confirmed":
            going_statuce = False
            try:
                time_diff = datetime.datetime.fromisoformat(
                    event["end"]['dateTime']) - \
                    datetime.datetime.fromisoformat(event["start"]['dateTime'])
            except BaseException:
                time_diff = "unknown_time"
            try:
                event_name = event["summary"]
            except BaseException:
                event_name = "unknown_event"
            try:
                for user_info in event["attendees"]:
                    if user_info["email"] == MY_EMAIL and user_info["responseStatus"] == "accepted":
                        going_statuce = True
            except BaseException:
                pass
        if going_statuce:
            approved_events.append({event_name: time_diff})
    return approved_events


def get_events_from_callendar(service, calendar_id, start_time, end_time):
    events_result = service.events().list(
        timeMin=start_time,
        timeMax=end_time,
        calendarId=calendar_id,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        logger('No upcoming events found.')
        approved_events = []
    else:
        approved_events = get_info_about_confirmed_events(events)
    return approved_events


def get_times(log_date):
    current_time = datetime.datetime.strptime(log_date, "%Y-%m-%d")
    start_time = datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        0,
        0,
        0).isoformat() + 'Z'
    end_time = datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        23,
        59,
        59).isoformat() + 'Z'
    return start_time, end_time


def get_meets(log_date):
    start_time, end_time = get_times(log_date)
    service = get_calendar_service()
    # Call the Calendar API
    logger('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    new_calendars = {}
    if not calendars:
        logger('No calendars found.')
    else:
        for calendar in calendars:
            summary = calendar['summary']
            call_id = calendar['id']
            if summary == MY_EMAIL:
                new_calendars.update(
                    {summary: get_events_from_callendar(service, call_id, start_time, end_time)})
    return new_calendars


if __name__ == '__main__':
    date = get_and_validate_date()
    print(get_meets(date))
