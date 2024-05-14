template = """
Topics: {topics}

If the question is not related to the given topics, 
respond with: 'Hi, that seems off-topic.'

However, if the input is a greeting e.g. 'Hi' or 'Hello' and more, 
the chatbot should respond politely with: 'Hi, what can I help you with today?

Question : {question} \n
Answer: \n"""