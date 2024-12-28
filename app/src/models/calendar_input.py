from typing import Optional
from pydantic import BaseModel, Field


class CalendarEventSearchInput(BaseModel):
    """Entradas para a função get_calendar_events"""

    max_result: int = Field(description="Número de eventos retornados ao consultar o Google Calendar. Padrão: 1")
    start_event: str = Field(
        description="""
            Data de início dos eventos a serem pesquisados. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )
    end_event: str = Field(
        description="""
            Data de término dos eventos a serem pesquisados. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )


class CalendarEventCreatorInput(BaseModel):
    """Entradas para a função create_calendar_event"""

    title: str = Field(description="Nome do evento")
    start_eventtime: str = Field(
        description="""
            Data de início do evento criado. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )
    end_eventtime: str = Field(
        description="""
            Data de fim do evento criado. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )
    timezone: str = Field(description="""Timezone em que o evento está sendo criado""")


class CalendarEventDeleteInput(BaseModel):
    """Entradas para a função delete_calendar_event"""

    event_id: str = Field(
        description="""
            O ID do evento recuperado do Google Calendar do usuário pelo buscador de eventos. Deve ser o ID completo.
        """
    )


class CurrentTimeInput(BaseModel):
    """Inputs for getting the current time"""

    pass


class TimeDeltaInput(BaseModel):
    """Inputs for getting time deltas"""

    delta_days: Optional[int] = Field(
        description="Number of days to add to the current time. Must be an integer.", default=0
    )
    delta_hours: Optional[int] = Field(
        description="Number of hours to add to the current time. Must be an integer.", default=0
    )
    delta_minutes: Optional[int] = Field(
        description="Number of minutes to add to the current time. Must be an integer.", default=0
    )
    delta_seconds: Optional[int] = Field(
        description="Number of seconds to add to the current time. Must be an integer.", default=0
    )


class SpecificTimeInput(BaseModel):
    """Inputs for setting a specific time"""

    year: int = Field(description="Year of the event")
    month: int = Field(description="Month of the event")
    day: int = Field(description="Day of the event")
    hour: int = Field(description="Hour of the event")
    minute: int = Field(description="Minute of the event")
