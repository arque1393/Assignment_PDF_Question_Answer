from pathlib import Path
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain_google_genai import GoogleGenerativeAI 
import google.generativeai as genai
import chromadb 
import os 

from config import DATABASE_PATH,FILE_STORE_PATH

#GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)



# Creating Embedding Function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def upload_on_vector_db(username : str, file_name:str, collection_name="default"):
    # Loading PDF Document 
    loader = PyPDFLoader(str((FILE_STORE_PATH/username/file_name).resolve()))
    # Splitting documents in pages
    pages = loader.load_and_split()
    # Extract Text and divide into smaller documents Chunks
    documents_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    documents = documents_splitter.split_documents(pages)
    # Chroma DB Client Database Path
    persist_dir = DATABASE_PATH/username
    if not persist_dir.exists():
        persist_dir.mkdir(parents=True)
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    try:
        _  = client.create_collection(name=collection_name)
    except : 
        raise Exception(f"Collection {collection_name} is exist") 

    langchain_chroma = Chroma( # Langchain Chroma Instance 
        client=client, collection_name=collection_name,
        embedding_function=embedding_function )

    langchain_chroma.from_documents(documents, embedding_function)

    return True
def get_collection_list(username : str):
    persist_dir = DATABASE_PATH/username
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    list_collection = client.list_collections()
    return [collection.name for collection in list_collection]

def get_retriever(username : str, collection:str):
    persist_dir = DATABASE_PATH/username
    if not persist_dir.exists():
        raise Exception(f"No directorr found as {username} ")
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    try:
        client.get_collection(collection)
    except:
        raise Exception(f"Collection {collection} not Found with this user {username}")
    chroma =  Chroma(
        client=client,
        collection_name=collection,
        embedding_function=embedding_function,
    )
    return chroma.as_retriever()

def get_answer(question:str,username:str, collection: str):
   
    retriever = get_retriever(username,collection)

    ## Retrive content form Document 
    docs = retriever.get_relevant_documents(question)
    
    # # # Model Selection     
    # model_name = r'models/chat-bison-001'
    model_name = r'models/text-bison-001'
    # model_name = r'models/gemini-pro'
    # model_name = r'models//gemini-pro-version'
    # model_name = r'models/aqa'

    llm = GoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)
    llm.invoke("Hello how are you ?")

    #  Question Answer Prompt Template 
    prompt_template = PromptTemplate.from_template('''
This is some information for your knoledge:
{knowledge}\n\n
Answer the given question from the previous content.
Question : {question}''')
    ## Define Dara Retrival Chain from Prompt template and llm models 
    chain = prompt_template | llm     
    answer = chain.invoke(
        {'knowledge':' '.join([page.page_content for page in docs]),
        'question':question})
    return answer