def node(state):
     
    # response = state["chains"]["off_topic"].invoke({"question": state["question"],
    #                         "topics": state["topics"]})
    response = """If the question is not related to the given topics, 
                  respond with: 'Hi, that seems off-topic.'

                 However, if the input is a greeting e.g. 'Hi' or 'Hello' and more, 
                 the chatbot should respond politely with: 'Hi, what can I help you with today?"""
    state['generation'] += [response]
    return {"generation": state["generation"]}