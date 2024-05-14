
def node(state):
    docs = state["retriever"].get_relevant_documents(state["question"])
    response = state["chains"]["retrieve"].invoke({"question": state["question"],
                            "context": docs})
    state['generation'] += [response]
    return {"generation": state["generation"]}