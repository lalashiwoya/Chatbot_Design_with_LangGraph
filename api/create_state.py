from typing_extensions import TypedDict, Dict
from typing import List
from langchain_core.memory import BaseMemory
from langchain_core.runnables import Runnable
from service.llama_index_retrive import RouterLlamaRetriever
### State

class GraphState(TypedDict):
    question : str
    generation : List[str]
    chat_history: BaseMemory
    worker_trace: List[str]
    workers: Dict
    retriever: RouterLlamaRetriever
    chains: Dict
    topics: List[str]
    model_name: str 
    