from typing import List
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from llama_index.core.schema import Document
from langchain_core.retrievers import BaseRetriever
from llama_index.core.embeddings import BaseEmbedding
from langchain.chat_models.base import  BaseChatModel
from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex
import os
from utils import init_llm_for_llama_index
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.tools import RetrieverTool
from llama_index.core.retrievers import RouterRetriever
from llama_index.core.selectors import (
    PydanticMultiSelector,
    PydanticSingleSelector,
)

    
def get_single_retriever(db_path: str,
                  embeddings_model: BaseEmbedding,
                  docs: List[Document],
                  chunk_size: int=360,
                  chunk_overlap: int=30,
                  top_k: int=3
                  ) -> BaseRetriever:
    # Settings.llm = init_llm_for_llama_index()
    Settings.embed_model = embeddings_model
    Settings.chunk_size = chunk_size
    Settings.chunk_overlap = chunk_overlap
    
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir=db_path)
    
    else:
        storage_context = StorageContext.from_defaults(persist_dir=db_path)
        index = load_index_from_storage(storage_context)
    
    retriever = index.as_retriever(similarity_top_k=top_k)
    return retriever

class RouterLlamaRetriever():
    def __init__(self, retrievers: List[BaseRetriever], retriever_descriptions: List[str]):
        self.retrievers = retrievers
        self.retriever_descriptions=retriever_descriptions
    
    def get_router_retriever(self):
        tools = []
        for retriever, description in zip(self.retrievers, self.retriever_descriptions):
            tool = RetrieverTool.from_defaults(
            retriever=retriever,
            description=(
                description
            ),
        )
            tools.append(tool)
        router_retriever = RouterRetriever(
            selector=PydanticSingleSelector.from_defaults(llm=init_llm_for_llama_index()),
            retriever_tools= tools
        )
        return router_retriever
    
    
    def get_relevant_documents(self, query: str) -> str:
        retriever = self.get_router_retriever()
        nodes = retriever.retrieve(query)
        final_output = ""
        for i, node in enumerate(nodes):
            url = node.metadata['doc_id']
            text = node.text
            url_with_text = f"Source: {i+1}, URL: {url}, \n\n Text: {text}"
            final_output += url_with_text + "\n"
        return final_output
        
    

    
    

    
    
    

# class LlamaRetriever(BaseRetriever):
#     embeddings_model: BaseEmbedding
#     db_path: str
#     docs: List[Document]
#     top_k: int=3
#     is_stored: bool = False
#     chunk_size: int=1024
    
    
    
#     def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> str:
#         retriever = self.get_retriever()
#         response = retriever.query(query['question'])
#         final_output = ""
#         for i, node in enumerate(response.source_nodes):
#             url = node.metadata['doc_id']
#             text = node.text
#             url_with_text = f"Source: {i+1}, URL: {url}, \n\n Text: {text}"
#             final_output += url_with_text + "\n"
#         return final_output
        
    
#     def get_retriever(self):
        
#         if not os.path.exists(self.db_path) or os.path.getsize(self.db_path) == 0:
            
#             Settings.llm = init_llm()
#             Settings.embed_model = self.embeddings_model
#             Settings.chunk_size = self.chunk_size
#             Settings.chunk_overlap = 30
            
#             index = VectorStoreIndex.from_documents(self.docs)
#             index.storage_context.persist(persist_dir=self.db_path)
            
#         else:
#             storage_context = StorageContext.from_defaults(persist_dir=self.db_path)
#             index = load_index_from_storage(storage_context)
            
#         retriever = index.as_query_engine(similarity_top_k=self.top_k)
        
#         return retriever
    
    
    
     
    