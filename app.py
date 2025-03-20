import getpass
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display
import warnings

warnings.filterwarnings("ignore")



def _set_env(var:str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("ANTHROPIC_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

def chatbot(state: State):
    return {"messages" : [llm.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

try:
    graph_image = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(graph_image)
    print("Graph saved as 'graph.png'. Open this file to view the graph.")
except Exception:
    print(f"An error occurred: {e}")