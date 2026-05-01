from langgraph.graph import StateGraph, START , END
from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages:Annotated[list,add_messages]



def sampleNode(state:State):
    return {"messages":["Sameple node message appended"]}



graph= StateGraph(State)
graph.add_node("first_node",sampleNode)
graph.add_edge(START,"first_node")
graph.add_edge("first_node",END)
graph =graph.compile()


response=graph.invoke(State({"messages":["hello this is the first message"]}))

print(response)