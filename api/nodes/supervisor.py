
def node(state):
    if len(state["worker_trace"]) >0:
        state["workers"].pop(state["worker_trace"][-1])
    if len(state["worker_trace"]) >0 and state["worker_trace"][-1] != "Off-Topic Expert" and "Off-Topic Expert" in state['workers']:
        state["workers"].pop("Off-Topic Expert")
    response = state["chains"]["supervisor"].invoke({"question": state["question"],
                         "initial_answer": state['generation'],
                         "workers": state["workers"],
                         "topics": state['topics'],
                         })
    state["worker_trace"] += [response]
    return {"worker_trace": state["worker_trace"], "workers": state["workers"]}