import os
from datetime import datetime
from typing_extensions import Literal

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import END
from langgraph.types import Command

from crew.tools import tools_list
from crew.prompts.calendar_assistant import CALENDAR_ASSISTANT_PROMPT
from crew.prompts.user_input import USER_PROMPT
from crew.utils.calendar_service import Calendar
from crew.graph.state import AgentState
from crew.utils.audio import AudioInfo


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
MODEL = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
TIMEZONE = Calendar().get_calendar_timezone()


def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


def get_next_node(last_message: BaseMessage, goto: str) -> str:
    if "TRANSCRIBE_AUDIO" in last_message.content:
        return goto
    return END


def calendar_node(state: AgentState) -> Command[Literal["transcribe_audio", END]]:  # type: ignore
    current_date: str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    current_week: str = datetime.now().strftime('%A')

    messages = [
        SystemMessage(CALENDAR_ASSISTANT_PROMPT),
        HumanMessage(USER_PROMPT.format(
            current_date=current_date,
            current_week=current_week,
            timezone=TIMEZONE
        ))
    ] + state["messages"]

    model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    caledar_agent = model.bind_tools(tools_list)
    result = caledar_agent.invoke(messages)

    goto = get_next_node(result, "transcribe_audio")

    return Command(
        update={
            "messages": result if goto == END else state
        },
        goto=goto
    )


def transcribe_audio_node(state: AgentState) -> Command[Literal["calendar_agent"]]:
    from openai import OpenAI

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
        goto="calendar_agent"
    )


calendar_tool_node = ToolNode(tools_list)
