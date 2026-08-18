from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessagesState, StateGraph

from .nodes import run_agent_reasoning, tool_nodes

load_dotenv()

AGENT_REASON="agent_reasoning"
ACT="act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    print(state['messages'][LAST])
    if not state['messages'][LAST].tool_calls:
        return END
    return ACT    


flow = StateGraph(MessagesState)
flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_nodes)

flow.add_conditional_edges(AGENT_REASON, should_continue, {END:END, ACT:ACT})

flow.add_edge(ACT, AGENT_REASON)


app= flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow_rover.png")




def main():
    print("Hello Rover again....")
    res = app.invoke({"messages": [HumanMessage(content="What is the weather in Kolkata? List it and then triple it")]})
    print(res["messages"][LAST].content)
