def node(state):
    response = state["chains"]["init_answer"].invoke({"question": state["question"],
                                 "chat_history": state["chat_history"]})
    state['generation'] = []
    state['generation'] += [response]
    
    return {'generation': state['generation'], "worker_trace": []}