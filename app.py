
import chainlit as cl
from utils import init_llm, init_memory
from api.create_chain import init_chain
from api.utils import get_router_retriever
from langchain.schema.runnable.config import RunnableConfig
from utils import read_configs_from_toml
from api.settings import init_settings
from api.create_workflow import custome_workflow
import os
from api.settings import set_user_settings_as_pydantic_model
from langchain.schema.runnable.config import RunnableConfig
from utils import custom_load_memory

from dotenv import load_dotenv
load_dotenv()

configs = read_configs_from_toml("config.toml")
tool_configs = read_configs_from_toml("tool_configs.toml")
retriever = get_router_retriever(configs)
graph = custome_workflow()
topics = configs['topics']['topics']

@cl.on_settings_update
def update_user_session(settings):
    user_settings = set_user_settings_as_pydantic_model(settings)
    
    if user_settings.llm_model_name:
        print("="*20)
        print(user_settings)
        cl.user_session.set("user_settings", user_settings)
        llm = init_llm(user_settings.llm_model_name)
        chains = init_chain(llm)
        cl.user_session.set("chains", chains)
        

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    test_username = os.getenv("APP_LOGIN_USERNAME")
    test_password = os.getenv("APP_LOGIN_PASSWORD")
    
    if (username, password) == (test_username, test_password):
        return cl.User(
            identifier="admin"
        )
    else:
        return None

@cl.on_chat_start
async def on_chat_start():
    initial_settings = init_settings()
    settings = await cl.ChatSettings(initial_settings).send()
    update_user_session(settings)
    llm = init_llm()
    memory = init_memory(llm, max_token_limit=configs['memory']['max_token_limit'])
    cl.user_session.set("memory", memory)

@cl.on_message
async def on_message(message: cl.Message):
    user_settings = cl.user_session.get("user_settings")
    chains = cl.user_session.get("chains")
    memory = cl.user_session.get("memory")
    workers = {tool_configs[tool]['name']: tool_configs[tool]["description"] for tool in tool_configs}
    
    # print(user_settings.llm_model_name)
    elements = []
    actions = []
    res = cl.Message(content="", elements=elements, actions=actions)
    response = ""
    print("5"*20)
    print(workers)
    input = {"question": message.content,
         "chat_history": memory,
         "workers": workers,
         "chains": chains,
         "retriever": retriever,
         "topics": topics}
    
    async for chunk in graph.astream(
        input, config=RunnableConfig(callbacks=[
                                        cl.LangchainCallbackHandler(
        stream_final_answer=True,
    )
                                        ])):
        
    #     content = chunk['messages'][0].content
    #     marker = "Final Answer:"
    #     if marker in content:
            
    #         response = content.split(marker)[-1].strip()
    # memory.save_context({"input": message.content}, {"output": response})
        if 'refine' in chunk:
            result = chunk['refine']['generation'][-1]
            await res.stream_token(result)
    
    # async for chunk in agent.astream({
    #     "question": message.content,
    #     "chat_history": memory,
    #     "topics": "\n".join(configs["topics"]["topics"])
    # }, config=RunnableConfig(callbacks=[
    #                                     cl.LangchainCallbackHandler(
    #     stream_final_answer=True,
    # )
    #                                     ])):
        
    #     content = chunk['messages'][0].content
    #     marker = "Final Answer:"
    #     if marker in content:
            
    #         response = content.split(marker)[-1].strip()

    # await res.send()
    
        
                    
        
             
        
           
    
    # async for chunk in agent.astream(
    #     {
    #         "question": message.content,
    #         "chat_history": memory,
    #         # "user_settings": user_settings,
    #         "topics": "\n".join(configs["topics"]["topics"])
             
    #     },
    #     config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    # ):
    #     # response.append(chunk)
    #     await res.stream_token(chunk)
    #     print("w"*10)
    #     print(chunk)
    # await res['ouptut'].send()
    # memory.chat_memory.add_user_message(message.content)
    # memory.chat_memory.add_ai_message(res.content)
    # memory.save_context({"input": message.content}, {"output": res.content})
    
    
 