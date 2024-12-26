from typing import Type
from datetime import datetime, timedelta

from pydantic import BaseModel
from langchain_core.tools import BaseTool

from src.functions.calendar import get_calendar_events, create_calendar_event, delete_calendar_event
from src.schemas.calendar import (
    CalendarEventSearchInput,
    CalendarEventCreatorInput,
    CurrentTimeInput,
    TimeDeltaInput,
    SpecificTimeInput,
    CalendarEventDeleteInput
)
from src.utils.calendar_service import Calendar


class GetCalendarEventsTool(BaseTool):
    name: str = "get_calendar_events"
    description: str = """
        Útil quando você deseja consultar eventos do Google Calendar em um intervalo específico de datas ou horários
    """
    args_schema: Type[BaseModel] = CalendarEventSearchInput

    def _run(
        self,
        max_result: int,
        start_event: str,
        end_event: str
    ):
        return get_calendar_events(
            Calendar().service,
            max_result,
            start_event,
            end_event
        )

    def _arun(self):
        raise NotImplementedError("get_calendar_events não suporta método asincrono")


class CreateCalendarEventTool(BaseTool):
    name: str = "create_calendar_event"
    description: str = """
        Útil quando você deseja criar/marcar/agendar um evento no Google Calendar em um intervalo específico de
        datas ou horários
    """
    args_schema: Type[BaseModel] = CalendarEventCreatorInput

    def _run(
        self,
        title: str,
        start_eventtime: str,
        end_eventtime: str,
        timezone: str
    ):
        return create_calendar_event(
            Calendar().service,
            title,
            start_eventtime,
            end_eventtime,
            timezone
        )

    def _arun(self):
        raise NotImplementedError("create_calendar_event não suporta método asincrono")


class DeleteCalendarEventTool(BaseTool):
    name: str = "delete_calendar_event"
    description: str = """
        Útil quando você deseja deletar um evento do Google Calendar através do ID do evento.
        Tenha certeza de passar o ID completo do evento
    """
    args_schema: Type[BaseModel] = CalendarEventDeleteInput

    def _run(
        self,
        event_id: str
    ):
        delete_calendar_event(Calendar().service, event_id)

    def _arun(self):
        raise NotImplementedError("delete_calendar_event does not support async")


class CurrentTimeTool(BaseTool):
    name: str = "get_current_time"
    description: str = """
        Útil quando você quer obter a data/horário atual no formato RFC3339 timestamp com time zone offset
        obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z
    """
    args_schema: Type[BaseModel] = CurrentTimeInput

    def _run(self):
        return (datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    def _arun(self):
        raise NotImplementedError("convert_time does not support async")


class TimeDeltaTool(BaseTool):
    name: str = "get_future_time"
    description: str = """
        Útil quando você quer obter a data/horário futura em RFC3339 timestamp, dado um time delta tal como
        1 day, 2 hours, 3 minutes, 4 seconds.
    """
    args_schema: Type[BaseModel] = TimeDeltaInput

    def _run(
        self,
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

    def _arun(self):
        raise NotImplementedError("get_future_time does not support async")


class SpecificTimeTool(BaseTool):
    name: str = "set_specific_time"
    description: str = """
        Útil quando você quer configurar uma data/hora específica para um evento.
        Por exemplo, quando você quer criar um evento as 3pm on June 3rd, 2021
    """
    args_schema: Type[BaseModel] = SpecificTimeInput

    def _run(
            self,
            year: int,
            month: int,
            day: int,
            hour: int,
            minute: int
    ):
        specific_time = datetime(year, month, day, hour, minute)
        return specific_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    def _arun(self):
        raise NotImplementedError("set_specific_time does not support async")
