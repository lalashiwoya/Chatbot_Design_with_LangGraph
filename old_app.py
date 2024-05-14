from utils import init_memory, init_llm
from api.create_chain import init_chain
from api.create_workflow import custome_workflow
from dotenv import load_dotenv
from api.utils import get_router_retriever
from utils import read_configs_from_toml
configs = read_configs_from_toml("config.toml")
retriever = get_router_retriever(configs)

load_dotenv(".env")

graph = custome_workflow()
llm = init_llm()
chains = init_chain(llm)
chat_history = init_memory(llm)

question="how to finetune LLM"


topics = ["Large Language Model(llm) finetuning", "Explanable AI", "Heart Disease"]
# workers = {tool_configs[tool]['name']: tool_configs[tool]["description"] for tool in tool_configs}
workers = {}
workers["LLM-XAI Knowledge Expert"] = """
An Expert in answering questions about Large language models (LLMs) and explainable AI (XAI).
"""

workers["Heart Disease Expert"] = """
An expert in diagnosing heart disease.
"""

workers["Off-Topic Expert"] = """
An Expert in answering questions beyond the given topics.
"""


input = {"question": question,
         "chat_history": chat_history,
         "workers": workers,
         "chains": chains,
         "retriever": retriever,
         "topics": topics}

events = graph.stream(
    
    input
)
for s in events:
    print(s)
    print("----")
 



