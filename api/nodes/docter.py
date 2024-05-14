
def node(state):
    response = state["chains"]["docter"].invoke({"question": state["question"]})
    state['generation'] += [response]
    return {"generation": state["generation"]}
    