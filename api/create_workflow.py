from langgraph.graph import END, StateGraph
from api.create_state import GraphState
from api.nodes import (
    docter,
    init_answer,
    off_topic,
    refine,
    retrieve,
    supervisor
)
from api.utils import normalize_expert_name



def custome_workflow():
    workflow = StateGraph(GraphState)
    workflow.add_node("initial_answer", init_answer.node)
    workflow.add_node("supervisor", supervisor.node)
    workflow.add_node("off_topic_answer", off_topic.node)
    workflow.add_node("retrieve", retrieve.node)
    workflow.add_node("docter", docter.node)
    workflow.add_node("refine", refine.node)

    workflow.set_entry_point("initial_answer")

    workflow.add_edge("initial_answer", "supervisor")
    workflow.add_conditional_edges("supervisor",
                    lambda x:x["worker_trace"][-1],
                    {"FINISH": "refine",
                    "Off-Topic Expert":"off_topic_answer",
                    "Heart Disease Expert":"docter",
                    "LLM-XAI Knowledge Expert":"retrieve"})

    workflow.add_edge("off_topic_answer", "refine")
    workflow.add_edge("refine", END)

    workflow.add_edge("retrieve", "supervisor")
    workflow.add_edge("docter", "supervisor")

    app = workflow.compile()
    
    return app