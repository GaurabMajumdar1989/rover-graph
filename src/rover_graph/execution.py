from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from .chains import generation_chain, reflection_chain

class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


REFLECT="reflect"
GENERATE="generate"

def generation_node(state: MessageGraph):
    return {"messages": [generation_chain.invoke({"messages": state["messages"]})]}

def reflection_node(state: MessageGraph):
    res = reflection_chain.invoke({"messages": state["messages"]})
### The notion is we are feeding back the previous LLM response as a HUman Message to the LLM again inspite of it being a AI Message because LLM also converse.
    return {"messages": [HumanMessage(content=res.content)]} 

def should_continue(state: MessageGraph) -> str:
    if len(state["messages"]) > 5:
        return END
    return REFLECT


def main():
    
    builder = StateGraph(state_schema=MessageGraph)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)
    builder.set_entry_point(GENERATE)
    builder.add_conditional_edges(GENERATE, should_continue, path_map={END:END, REFLECT:REFLECT})
    builder.add_edge(REFLECT, GENERATE)

    graph = builder.compile()


    inputs = {
        "messages": [
            HumanMessage(
                content="""
    Make this tweet better
    @AI
    AI advent will doom humans in the far future and it has already started showing symptoms.
    """
            )
        ]
    }

    # graph.get_graph().draw_mermaid_png(output_file_path="flow_rover.png")
    # graph.get_graph().print_ascii()
    response = graph.invoke(inputs)
    print(response["messages"][-1].content)



