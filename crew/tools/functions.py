from langchain.tools import tool
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
from crew.tools.models import (
    CalendarEventSearchInput,
    CalendarEventCreatorInput,
    CalendarEventDeleteInput,
    CurrentTimeInput,
    TimeDeltaInput,
    SpecificTimeInput,
    CalendarEventSearchOutput,
    CalendarEventCreatorOutput
)
from crew.utils.calendar_service import Calendar

SCOPES = ["https://www.googleapis.com/auth/calendar"]

service = Calendar().service


@tool("get-calendar-events-tool", args_schema=CalendarEventSearchInput)
def get_calendar_events(max_result, start_event, end_event):
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


@tool("create-calendar-events-tool", args_schema=CalendarEventCreatorInput)
def create_calendar_event(title, start_event, end_event, timezone):
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


@tool("delete-calendar-events-tool", args_schema=CalendarEventDeleteInput)
def delete_calendar_event(event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()

        return "Evento deletado com sucesso"
    except HttpError as error:
        raise HttpError(f"An error occurred: {error}")


@tool("get-current-time-tool", args_schema=CurrentTimeInput)
def get_current_time():
    return (datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))


@tool("get-future-time-tool", args_schema=TimeDeltaInput)
def get_future_time(
    delta_days: int = 0,
    delta_hours: int = 0,
    delta_minutes: int = 0,
    delta_seconds: int = 0
):
    current = (
        datetime.now()
        .replace(hour=delta_hours or 0)
        .replace(minute=delta_minutes or 0)
        .replace(second=delta_seconds or 0)
    )
    return (
        current + timedelta(
            days=delta_days or 0,
            hours=3
        )
    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


@tool("set-specific-time-tool", args_schema=SpecificTimeInput)
def set_specific_time(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute).strftime("%Y-%m-%dT%H:%M:%S%z")
