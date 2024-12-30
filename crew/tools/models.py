from typing import Optional
from pydantic import BaseModel, Field


class CalendarEventSearchInput(BaseModel):
    """
        Útil quando você deseja consultar eventos do Google Calendar em um intervalo específico de datas ou horários
    """

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
    """
        Útil quando você deseja criar/marcar/agendar um evento no Google Calendar em um intervalo específico de
        datas ou horários
    """

    title: str = Field(description="Nome do evento")
    start_event: str = Field(
        description="""
            Data de início do evento criado. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )
    end_event: str = Field(
        description="""
            Data de fim do evento criado. Deve ser um timestamp no formato RFC3339 com deslocamento
            de fuso horário obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z.
        """
    )
    timezone: str = Field(description="""Timezone em que o evento está sendo criado""")


class CalendarEventDeleteInput(BaseModel):
    """
        Útil quando você deseja deletar um evento do Google Calendar através do ID do evento.
        Tenha certeza de passar o ID completo do evento
    """

    event_id: str = Field(
        description="""
            O ID do evento recuperado do Google Calendar do usuário pelo buscador de eventos. Deve ser o ID completo.
        """
    )


class CurrentTimeInput(BaseModel):
    """
        Útil quando você quer obter a data/horário atual no formato RFC3339 timestamp com time zone offset
        obrigatório. Exemplos: 2024-01-01T00:00:00-07:00 ou 2024-01-01T00:00:00Z
    """

    pass


class TimeDeltaInput(BaseModel):
    """
        Útil quando você quer obter a data/horário futura em RFC3339 timestamp, dado um time delta tal como
        1 day, 2 hours, 3 minutes, 4 seconds.
    """

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
    """
        Útil quando você quer configurar uma data/hora específica para um evento.
        Por exemplo, quando você quer criar um evento as 3pm on June 3rd, 2021
    """

    year: int = Field(description="Year of the event")
    month: int = Field(description="Month of the event")
    day: int = Field(description="Day of the event")
    hour: int = Field(description="Hour of the event")
    minute: int = Field(description="Minute of the event")


class CalendarEventCreatorOutput(BaseModel):
    """Informações referentes ao evento criado no Google Calendar"""

    title: str = Field(description="Título do evento criado")
    event: dict = Field(description="Informações extras referentes ao evento criado")


class CalendarEventSearchOutput(BaseModel):
    """Lista de eventos no Google Calendar relacionado ao email"""

    email: str = Field(description="Email do usuário do Google Calendar")
    events: list = Field(description="Lista de eventos")
