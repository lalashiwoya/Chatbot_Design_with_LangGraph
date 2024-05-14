def node(state):
     
    response = state["chains"]["off_topic"].invoke({"question": state["question"],
                            "topics": state["topics"]})
    state['generation'] += [response]
    return {"generation": state["generation"]}