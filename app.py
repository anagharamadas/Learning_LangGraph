import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display
import warnings
from langchain_community.chat_models import ChatPerplexity
#from langchain_tavily import TavilySearch
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv


warnings.filterwarnings("ignore")

"""
# Load environment variables from .env file
load_dotenv()

os.environ["PPLX_API_KEY"] = os.getenv("PPLX_API_KEY")



chat = ChatPerplexity(
        temperature=0, 
        pplx_api_key=os.environ["PPLX_API_KEY"],
        model="sonar-pro"
        )



class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


#llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

def chatbot(state: State):
    return {"messages" : [chat.invoke(state["messages"])]}


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

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages" : [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye")
            break
        stream_graph_updates(user_input)
    except Exception:
        user_input = "What do you know about LangGraph?"
        print("User:" + user_input)
        stream_graph_updates(user_input)
        break  

"""   



# Load environment variables from .env file
load_dotenv()

# Set API key as an environment variable
os.environ["TAVILY_API_KEY"] = os.getenv("TAVIL_API_KEY")





tool = TavilySearchResults(
        max_results=5,
        topic="general",
        tavily_api_key=os.environ["TAVILY_API_KEY"]
)


model_generated_tool_call = {
    "args": {"query": "What happened at the last wimbledon"},
    "id": "1",
    "name": "tavily",
    "type": "tool_call",
}

tool_msg = tool.invoke(model_generated_tool_call)

print(tool_msg.content[:400])




