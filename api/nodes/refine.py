def node(state):
    response = state["chains"]["refine"].invoke({"question": state["question"],
                                    "chat_history": state["chat_history"],
                                    "topics": state["topics"],
                                    "answer": state["generation"],
                                    "model_name": state["model_name"]
                                                        })
    state['generation'] += [response]
    return {"generation": state["generation"]}