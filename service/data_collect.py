# from legacy_api.chains.clean_texts_from_url_chain import create_clean_texts_from_url_chain
from langchain_core.runnables.base import RunnableSequence
from typing import List
from langchain.chat_models.base import  BaseChatModel
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.web import SimpleWebPageReader
from langchain_openai import ChatOpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader

# class DocumentRefiner:
#     def __init__(self, llm: BaseChatModel,
#                  chunk_size:int = 3000, 
#                  chunk_overlap:int = 0):
#         self.chain = create_clean_texts_from_url_chain(llm)
#         self.chunk_size = chunk_size
#         self.chunk_overlap = chunk_overlap

#     def get_sentence_splitter(self):
#         return SentenceSplitter(
#             chunk_size=self.chunk_size,
#             chunk_overlap=self.chunk_overlap,
#         )

#     def refine_html_files(self, docs: List[Document]) -> List[Document]:
#         cleaned_docs = []
#         splitter = self.get_sentence_splitter()
#         for doc in docs:
#             cleaned_doc_segments = ""
#             doc_segments = splitter.get_nodes_from_documents([doc])

#             for seg in doc_segments:
#                 try:
#                     response = self.chain.invoke({"question": seg.text})
#                     cleaned_doc_segments += response + "\n"
#                 except Exception as e:
#                     print(f"Error processing segment: {e}")

#             doc.text = cleaned_doc_segments
#             cleaned_docs.append(doc)

#         return cleaned_docs

class PagesToDocuments:
    def __init__(self, path: str,
                #  clean_texts: bool = False,
                 chunk_size: int = 3000,
                 chunk_overlap: int = 0):
        self.path = path
        self.chunk_size = chunk_size
        self.chuck_overlap = chunk_overlap
        
        # self.llm = init_llm()
        # self.text_cleaner = DocumentRefiner(self.llm, 
        #                                     chunk_size= chunk_size,
        #                                     chunk_overlap=chunk_overlap)
        # self.clean_texts = clean_texts
        self.docs = self.get_all_documents()
        
        def get_all_documents(self) -> List[Document]:
            pass
        

class WebPagesToDocuments(PagesToDocuments):
    def __init__(self, path: str,
                #  clean_texts: bool = False,
                 chunk_size:int = 3000,
                 chunk_overlap:int = 0):
        super().__init__(path, chunk_size, chunk_overlap)
        self.docs = self.get_all_documents()
    
    def get_document_from_url(self, url:str) -> Document:
        doc = SimpleWebPageReader(html_to_text=True).load_data(
        [url])[0]
        doc.metadata['doc_id'] = doc.doc_id
        return doc
        
    def get_all_documents(self) -> List[Document]:
        docs = []
        with open(self.path) as file:
            urls = file.read().splitlines()
        for url in urls:
            docs.append(self.get_document_from_url(url))
        
        # if self.clean_texts:
        #     docs = self.text_cleaner.refine_html_files(docs)
        return docs

class PdfPagesToDocuments(PagesToDocuments):
      def __init__(self, path: str,
                #  clean_texts: bool = False,
                 chunk_size:int = 3000,
                 chunk_overlap:int = 0):
        super().__init__(path, chunk_size, chunk_overlap)
        self.docs = self.get_all_documents()
    
      def get_all_documents(self) -> List[Document]:
         docs = SimpleDirectoryReader(self.path).load_data()
         for doc in docs:
            doc.metadata['doc_id'] = doc.metadata['file_path']
        #  if self.clean_texts:
        #     docs = self.text_cleaner.refine_html_files(docs)
         return docs

class YoutubePagesToDocuments(PagesToDocuments):
      def __init__(self, path: str,
                #  clean_texts: bool = False,
                 chunk_size:int = 3000,
                 chunk_overlap:int = 0):
        super().__init__(path, chunk_size, chunk_overlap)
        self.docs = self.get_all_documents()
     
      def get_document_from_url(self, url:str) -> Document:
            loader = YoutubeTranscriptReader()
            doc = loader.load_data(
                ytlinks=[url]
            )[0]
            
            doc.metadata['doc_id'] = url
            return doc
    
      def get_all_documents(self) -> List[Document]:
            docs = []
            with open(self.path) as file:
                urls = file.read().splitlines()
            for url in urls:
                docs.append(self.get_document_from_url(url))
            
            # if self.clean_texts:
            #     docs = self.text_cleaner.refine_html_files(docs)
            return docs
         


