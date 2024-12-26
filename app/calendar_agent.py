import os
from datetime import datetime

from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

from src.prompts.calendar_assistant import ASSISTANT_PROMPT, USER_PROMPT
from src.tools.calendar import (
    GetCalendarEventsTool,
    CreateCalendarEventTool,
    DeleteCalendarEventTool,
    TimeDeltaTool,
    SpecificTimeTool
)
from src.utils.calendar_service import Calendar

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")


def invoke_agent(user_input: str, timezone: str):
    llm = ChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
    tools = [
        GetCalendarEventsTool(),
        CreateCalendarEventTool(),
        DeleteCalendarEventTool(),
        TimeDeltaTool(),
        SpecificTimeTool(),
    ]
    current_date: str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    current_week: str = datetime.now().strftime('%A')

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(ASSISTANT_PROMPT),
            HumanMessage(USER_PROMPT.format(
                current_date=current_date,
                current_week=current_week,
                timezone=timezone,
                user_input=user_input,
            )),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    functions = [convert_to_openai_function(t) for t in tools]
    llm_with_tools = llm.bind(functions=functions)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)
    result = agent_executor.invoke({"input": input})

    return result.get("output")


def receive_message():
    timezone = Calendar().get_calendar_timezone()

    while True:
        message = input("Você: ")
        if message.lower() == "sair":
            print("Encerrando o chat...", flush=True)
            break
        output = invoke_agent(message, timezone)
        print(f"Assistente: {output}")


if __name__ == "__main__":
    receive_message()
