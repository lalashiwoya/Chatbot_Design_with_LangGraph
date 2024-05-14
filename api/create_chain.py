from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from api.prompts import (
    docter,
    init_answer,
    off_topic,
    refine,
    retrieve,
    supervisor
)

def create_chain(template, llm):
    chain = (ChatPromptTemplate.from_template(template) | llm | StrOutputParser())
    return chain

def init_chain(llm):
    docter_chain = create_chain(docter.template, llm)
    init_answer_chain = create_chain(init_answer.template, llm)
    off_topic_chain = create_chain(off_topic.template, llm)
    refine_chain = create_chain(refine.template, llm)
    retrieve_chain = create_chain(retrieve.template, llm)
    supervisor_chain = create_chain(supervisor.template, llm)
    return {"docter": docter_chain,
            "init_answer": init_answer_chain,
            "off_topic": off_topic_chain,
            "refine": refine_chain,
            "retrieve": retrieve_chain,
            "supervisor": supervisor_chain}
    


 