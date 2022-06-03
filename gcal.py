# https://developers.google.com/calendar/api/quickstart/python
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def filter(events: list) -> list:
    in_a_week = []
    week = datetime.datetime.now() + datetime.timedelta(days=2)
    for i in events:
        i = i.split(" ")[0]
        i = datetime.datetime.strptime(i, "%Y-%m-%d")
        if i < week:
            i = str(i).replace("00:00:00", "")
            in_a_week.append(i)

    # HACK:
    events = events[:len(in_a_week)]
    events = [str(i).replace("00:00:00", "") for i in events]

    return events


def get_events() -> list[str]:
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    l = []
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
          maxResults=10, singleEvents=True,
          orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        # Prints the start and name of the next 10 events
        # TODO: get events that are in a week or less using datetime
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))

            start = start.split("T")[0]

            start = datetime.datetime.strptime(start, "%Y-%m-%d")

            # HACK:
            l.append(str(start) + " " + event['summary'])
            

    except HttpError as error:
        print('An error occurred: %s' % error)

    return l



if __name__ == '__main__':
    print(get_events())
