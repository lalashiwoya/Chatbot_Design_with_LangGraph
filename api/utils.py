from service.data_collect import WebPagesToDocuments, PdfPagesToDocuments, YoutubePagesToDocuments
# from llama_index.embeddings.openai import OpenAIEmbedding
from service.llama_index_retrive import RouterLlamaRetriever, get_single_retriever
from utils import read_configs_from_toml, init_sentence_embedding


def collect_docs_from_a_single_domain(configs, key_word):
    # try:
    #     clean_texts=configs["dataset"][key_word]["if_clean_texts"]
    # except:
    #     print("You don't specify if you want to clean the original texts or not in the configuration file")
    
    try: 
        path = configs["dataset"][key_word]["url_path"]
        web_docs = WebPagesToDocuments(path = path, 
                            ).docs
    except:
        print(f"You don't have any resources from the web page regarding {key_word}")
        web_docs = []
        
    try:
        path = configs["dataset"][key_word]["pdf_dir"]
        pdf_docs = PdfPagesToDocuments(path = path,
                                   ).docs
    except:
        print(f"You don't have any resources from the local pdfs regarding {key_word}")
        pdf_docs = []
    
    try:
        path = configs["dataset"][key_word]["youtube_urls"]
        youtube_docs = YoutubePagesToDocuments(path = path,
                                   ).docs
    except:
        print(f"You don't have any resources from the youtube subtitles regarding {key_word}")
        youtube_docs = [] 
    docs = web_docs + pdf_docs + youtube_docs
    
    if len(docs) > 0:
        return docs
    else:
        raise ValueError(f"No resource found for your qa chain regarding {key_word}")


def build_retriever_from_source_path(configs, key_word):
    docs = collect_docs_from_a_single_domain(configs, key_word)
    retriever = get_single_retriever(db_path=configs["dataset"][key_word]["db_path"],
                            chunk_size = configs["llama_index"]["chunk_size"],
                            embeddings_model=init_sentence_embedding(configs["llama_index"]["sentence_transformer"]),
                            chunk_overlap=configs["llama_index"]["chunk_overlap"],
                            docs = docs)
    return retriever
        
        

def get_router_retriever(configs: dict):

    # configs = read_configs_from_toml(path)

    # path = "data/llm_finetune/urls/urls.txt"
    # if_clean_texts = False
    # llm_docs = collect_docs_from_a_single_domain(configs, "llm_finetune")
    # llm_retriever = get_single_retriever(db_path=configs["dataset"]["llm_finetune"]["db_path"],
    #                         chunk_size = configs["llama_index"]["chunk_size"],
    #                         embeddings_model=init_sentence_embedding(),
    #                         chunk_overlap=configs["llama_index"]["chunk_overlap"],
    #                         docs = llm_docs)
    retrievers = []
    descriptions = []
    for topic in configs['dataset']:
        docs = collect_docs_from_a_single_domain(configs, topic)
        retriever = get_single_retriever(db_path=configs["dataset"][topic]["db_path"],
                            chunk_size = configs["llama_index"]["chunk_size"],
                            embeddings_model=init_sentence_embedding(),
                            chunk_overlap=configs["llama_index"]["chunk_overlap"],
                            docs = docs)
        description = configs["dataset"][topic]["retriever_description"]
        retrievers.append(retriever)
        descriptions.append(description)

        
    # llm_retriever = build_retriever_from_source_path(configs, "llm_finetune") 
    # llm_retriever_description = "Will retrieve all context regarding llm finetuning"
    
    # # explainable_ai_docs = collect_docs_from_a_single_domain(configs, "explainable_ai")
    # # explainable_ai_retriever = get_single_retriever(db_path=configs["dataset"]["explainable_ai"]["db_path"],
    # #                         chunk_size = configs["llama_index"]["chunk_size"],
    # #                         embeddings_model=init_sentence_embedding(),
    # #                         docs = explainable_ai_docs)
    # explainable_ai_retriever = build_retriever_from_source_path(configs, "explainable_ai")
    # explainable_ai_description = "Will retrieve all context regarding explainable ai"
    
    router_retriver = RouterLlamaRetriever(retrievers,
                                     descriptions)
    # relevant_docs = router_retriver.get_relevant_documents(query)
    return router_retriver
    

    # llm_web_docs = WebPagesToDocuments(path = configs["dataset"]["llm_finetune"]["url_path"], 
    #                         clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    # llm_pdf_docs = PdfPagesToDocuments(path = configs["dataset"]["llm_finetune"]["pdf_dir"],
    #                                clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    # llm_youtube_docs = YoutubePagesToDocuments(path = configs["dataset"]["llm_finetune"]["youtube_urls"], 
    #                                        clean_texts=configs["dataset"]["llm_finetune"]["if_clean_texts"]).docs
    
    # llm_docs = llm_web_docs + llm_pdf_docs + llm_youtube_docs
    

    # llm_retriever = get_single_retriever(db_path=configs["dataset"]["llm_finetune"]["db_path"],
    #                         chunk_size = configs["llama_index"]["chunk_size"],
    #                         embeddings_model=OpenAIEmbedding(model="text-embedding-3-small"),
    #                         docs = llm_docs)
    # llm_retriever_description = "Will retrieve all context regarding llm finetuning"
    
    
    # router_retriver = RouterLlamaRetriever([llm_retriever],
    #                                  [llm_retriever_description])
    # # relevant_docs = router_retriver.get_relevant_documents(query)
    # return router_retriver
    



