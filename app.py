import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
import json
#from langchain_anthropic import ChatAnthropic
from IPython.display import Image, display
import warnings
from langchain_community.chat_models import ChatPerplexity
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv


warnings.filterwarnings("ignore")


# Load environment variables from .env file
load_dotenv()

os.environ["PPLX_API_KEY"] = os.getenv("PPLX_API_KEY")

# Load environment variables from .env file
load_dotenv()

# Set API key as an environment variable
os.environ["TAVILY_API_KEY"] = os.getenv("TAVIL_API_KEY")





tools = TavilySearchResults(
        max_results=5,
        topic="general",
        tavily_api_key=os.environ["TAVILY_API_KEY"]
)


llm = ChatPerplexity(
        temperature=0, 
        pplx_api_key=os.environ["PPLX_API_KEY"],
        model="sonar-pro"
        )



class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


llm_with_tools = llm.bind_tools(tools)
def chatbot(state: State):
    return {"messages" : [llm_with_tools.invoke(state["messages"])]}

class BasicToolNode:

    def __init__(self, tools:list) -> None:
                 self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs:dict):
        if messages := inputs.get("messages", []):
              message = messages[-1]
        else:
             raise ValueError("No messages found in inputs")
        outputs = []
        for tool_call in message.tool_calls:
             tool_result = self.tools_by_name[tool_call["name"]].invoke(
                  tool_call["args"]
             )
             outputs.append(
                  ToolMessage(
                       content=json.dumps(tool_result),
                       name=tool_call["name"],
                       tool_call_id=tool_call["id"],
                  )
             )
        return {"messages": outputs}


tool_node = BasicToolNode(tools=[tools])
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")

graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


def route_tools(
          state: State,
):
    if isinstance(state, list):
        ai_message = state[-1]

    elif messages:= state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    
    return END

graph_builder.add_conditional_edges(
     "chatbot",
     route_tools,


     {"tools" : "tools", END:END},
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
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

model_generated_tool_call = {
    "args": {"query": "What happened at the last wimbledon"},
    "id": "1",
    "name": "tavily",
    "type": "tool_call",
}

tool_msg = tool.invoke(model_generated_tool_call)

print(tool_msg.content[:400])

"""


