from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory, ConversationTokenBufferMemory
from langchain_core.memory import BaseMemory
from langchain.chat_models.base import  BaseChatModel
from llama_index.llms.openai import OpenAI
import toml
# from langchain_community.llms import LlamaCpp
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler


def init_llm(model_name = "gpt-3.5-turbo"):
    if "gpt" in model_name:
        llm = ChatOpenAI(temperature=0, model_name = model_name, streaming = True,
                         callbacks=[FinalStreamingStdOutCallbackHandler(answer_prefix_tokens=["Final", "Answer"])])
    # elif "llama" in model_name:
    
    #     llm = LlamaCpp(
    #     model_path="llama_models/llama-2-7b-chat.Q4_0.gguf",
    #     temperature=0,
    #     verbose=True,   
    #     streaming = True
    # )
    return llm

def init_llm_for_llama_index(model_name: str= "gpt-3.5-turbo"):
    llm = OpenAI(temperature=0, model_name = model_name, streaming = True)
    return llm

def init_memory(llm: BaseChatModel, max_token_limit:int = 500) -> BaseMemory:
    # memory = ConversationBufferMemory(return_messages = True)
    memory = ConversationSummaryBufferMemory(return_messages = True,
                                            max_token_limit= max_token_limit,
                                            llm = llm)
    return memory
    


def custom_load_memory(memory: BaseMemory) -> str:
    return str(memory.load_memory_variables({})['history'])

def read_configs_from_toml(path: str) -> dict:
    with open(path, 'r') as toml_file:
        data = toml.load(toml_file)
    return data

def init_sentence_embedding(model_name = "text-embedding-3-small"):
    return OpenAIEmbedding(model=model_name)


 
        
 