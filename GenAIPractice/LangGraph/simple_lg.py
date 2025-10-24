from typing_extensions import TypedDict

#Defining a type checking state class
class State(TypedDict):
    graph_state: str

#Definig nodes that take the initial state and append a new message
def node_1(state):
    print("--Node 1--")
    return {"graph_state": state["graph_state"] + "I am"}

def node_2(state):
    print("--Node 2--")
    return {"graph_state": state["graph_state"] + " Happy"}

def node_3(state):
    print("--Node 3--")
    return {"graph_state": state["graph_state"] + " Sad"}

import random
from typing import Literal

#A ranond mood decide to choose which node to append to the intial state
def decide_mood(state) -> Literal["node_2", "node_3"]:

    user_input = state["graph_state"]

    if random.random() < 0.5:
        return "node_2"
    
    return "node_3"

from langgraph.graph import StateGraph, START, END

#Buidling the graph
builder = StateGraph(State)
#Adding nodes to the graph
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

#Adding the edges or the logic that decides which node to choose
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

#Compiling the graph
graph = builder.compile()

# Invoking the graph and capturing the result
final_state = graph.invoke({"graph_state": "Hi, this is Lance."})

# Printing the final state
print(final_state["graph_state"])

