from langgraph.graph import StateGraph, MessagesState, START
from src.graph.nodes import calendar_node, transcribe_audio_node


def get_graph():
    workflow = StateGraph(MessagesState)
    workflow.add_node("calendar", calendar_node)
    workflow.add_node("transcribe_audio", transcribe_audio_node)

    workflow.add_edge(START, "calendar")
    return workflow.compile()
