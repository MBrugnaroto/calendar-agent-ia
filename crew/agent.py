from langgraph.graph import StateGraph, END
from crew.graph.nodes import (
    calendar_node,
    calendar_tool_node,
    should_continue,
    transcribe_audio_node
)
from crew.graph.state import AgentState


workflow = StateGraph(AgentState)

workflow.add_node("calendar_agent", calendar_node)
workflow.add_node("calendar_actions", calendar_tool_node)
workflow.add_node("transcribe_audio", transcribe_audio_node)

workflow.set_entry_point("calendar_agent")
workflow.add_conditional_edges(
    "calendar_agent",
    should_continue,
    {
        "transcribe": "transcribe_audio",
        "execute_tool": "calendar_actions",
        "end": END,
    },
)
workflow.add_edge("transcribe_audio", "calendar_agent")
workflow.add_edge("calendar_actions", "calendar_agent")

graph = workflow.compile()
graph.name = "CalendarWorkflow"
