from googleapiclient.errors import HttpError
from src.schemas.calendar import (
    CalendarEventSearchOutput,
    CalendarEventCreatorOutput
)


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_events(service, max_result, start_event, end_event):
    try:
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_event,
                timeMax=end_event,
                maxResults=max_result,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        events_summary = []

        for event in events:
            events_summary.append(
                {
                    "event_id": event.get("id"),
                    "event_name": event.get("summary"),
                    "start_event": event.get("start").get("dateTime"),
                    "end_event": event.get("end").get("dateTime")
                }
            )

        return CalendarEventSearchOutput(
            email=events_result.get("summary", None),
            events=events_summary
        )

    except HttpError as error:
        raise HttpError(f"An error occurred: {error}")


def create_calendar_event(service, title, start_event, end_event, timezone):
    event = {
        'summary': title,
        'start': {
            'dateTime': start_event,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_event,
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    try:
        service.events().insert(calendarId="primary", body=event).execute()

        return CalendarEventCreatorOutput(
            title=title,
            event=event
        )

    except HttpError as error:
        raise HttpError(f"An error occurred: {error}")


def delete_calendar_event(service, event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()

        return "Evento deletado com sucesso"
    except HttpError as error:
        raise HttpError(f"An error occurred: {error}")
