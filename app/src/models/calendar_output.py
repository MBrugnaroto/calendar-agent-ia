from pydantic import BaseModel, Field


class CalendarEventCreatorOutput(BaseModel):
    """Informações referentes ao evento criado no Google Calendar"""

    title: str = Field(description="Título do evento criado")
    event: dict = Field(description="Informações extras referentes ao evento criado")


class CalendarEventSearchOutput(BaseModel):
    """Lista de eventos no Google Calendar relacionado ao email"""

    email: str = Field(description="Email do usuário do Google Calendar")
    events: list = Field(description="Lista de eventos")
