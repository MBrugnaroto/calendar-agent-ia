import os
from datetime import datetime
from typing_extensions import Literal

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState, END
from langgraph.types import Command

from src.prompts.calendar import ASSISTANT_PROMPT, USER_PROMPT
from src.tools.calendar import (
    GetCalendarEventsTool,
    CreateCalendarEventTool,
    DeleteCalendarEventTool,
    TimeDeltaTool,
    SpecificTimeTool,
)
from src.utils.calendar_service import Calendar


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
MODEL = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
TIMEZONE = Calendar().get_calendar_timezone()


def get_next_node(last_message: BaseMessage, goto: str):
    if "TRANSCRIBE_AUDIO" in last_message.content:
        return goto
    return END


def calendar_node(state: MessagesState) -> Command[Literal["transcribe_audio", END]]:  # type: ignore
    tools = [
        GetCalendarEventsTool(),
        CreateCalendarEventTool(),
        DeleteCalendarEventTool(),
        TimeDeltaTool(),
        SpecificTimeTool()
    ]
    current_date: str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    current_week: str = datetime.now().strftime('%A')

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(ASSISTANT_PROMPT),
            HumanMessage(USER_PROMPT.format(
                current_date=current_date,
                current_week=current_week,
                timezone=TIMEZONE
            )),
            ("placeholder", "{messages}"),
        ]
    )

    def _modify_state_messages(state: AgentState):
        return prompt.invoke({"messages": state["messages"]}).to_messages()

    caledar_agent = create_react_agent(
        MODEL, tools, state_modifier=_modify_state_messages
    )

    result = caledar_agent.invoke(state)
    goto = get_next_node(result["messages"][-1], "transcribe_audio")

    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="calendar"
    )

    return Command(
        update={
            "messages": result["messages"] if goto == END else state["messages"]
        },
        goto=goto
    )


def transcribe_audio_node(state: MessagesState) -> Command[Literal["calendar"]]:
    from openai import OpenAI
    from src.utils.audio_recorder import AudioInfo

    audio: AudioInfo = eval(state['messages'][-1].content)

    audio_file = open(f"{audio.path}/{audio.name}", "rb")
    transcription = OpenAI().audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )

    return Command(
        update={
            "messages": [HumanMessage(transcription.text)]
        },
        goto="calendar"
    )
