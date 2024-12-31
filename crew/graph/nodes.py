import os
from datetime import datetime

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from crew.tools import tools_list
from crew.prompts.calendar_assistant import CALENDAR_ASSISTANT_PROMPT
from crew.prompts.user_input import USER_PROMPT
from crew.utils.calendar_service import Calendar
from crew.graph.state import AgentState
from crew.utils.audio import AudioInfo


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
MODEL = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
CALENDAR_AGENT = MODEL.bind_tools(tools_list)
TIMEZONE = Calendar().get_calendar_timezone()


def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]

    if "AudioInfo" in last_message.content:
        return "transcribe"

    if not last_message.tool_calls:
        return "end"

    return "execute_tool"


def is_audio(last_message: BaseMessage) -> str:
    if "TRANSCRIBE_AUDIO" in last_message.content:
        return True
    return False


def calendar_node(state: AgentState):
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

    result = CALENDAR_AGENT.invoke(messages)

    return {
        "messages": state["messages"] if is_audio(result) else result
    }


def transcribe_audio_node(state: AgentState):
    from openai import OpenAI

    audio: AudioInfo = eval(state['messages'][-1].content)

    audio_file = open(f"{audio.path}/{audio.name}", "rb")
    transcription = OpenAI().audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )

    return {
        "messages": [HumanMessage(transcription.text)]
    }


calendar_tool_node = ToolNode(tools_list)
