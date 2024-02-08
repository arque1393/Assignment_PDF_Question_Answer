from pathlib import Path
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_google_genai import GoogleGenerativeAIEmbeddings

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
# embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def upload_on_vector_db(username : str, file_name:str, collection_name="default"):
    """ 
    Upload content of a pdf file in Vector Database as knowledge space of an AI.
    Args:
        username (str): To access specific user data
        file_name (str): To locate exact file
        collection_name (str, optional): _description_. Defaults to "default".
    Raises:
        Exception: user name not found  or collection not found 
    Returns:
        Bool:True on success
    """
    # Loading PDF Document 
    loader = PyPDFLoader(str((FILE_STORE_PATH/username/file_name).resolve()))
    # Splitting documents in pages
    pages = loader.load_and_split()
    # Extract Text and divide into smaller documents Chunks
    documents_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
    documents = documents_splitter.split_documents(pages)
    print(documents)
    # Chroma DB Client Database Path
    persist_dir = DATABASE_PATH/username
    print(persist_dir)
    if not persist_dir.exists():
        persist_dir.mkdir(parents=True)
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    try:
        _  = client.create_collection(name=collection_name)
    except : 
        raise Exception(f"Collection {collection_name} is exist") 

    Chroma.from_documents(documents=documents,collection_name=collection_name,
                    embedding=embedding_function, 
                    persist_directory=persist_dir.resolve().as_posix())

    
    return True

def get_collection_list(username : str):
    """ To get all Collection name of a particular user
    Args:
        username (str): To fetch Specific User;s Collection
    Returns:
        List[str] :  List of name of collections 
    """
    persist_dir = DATABASE_PATH/username
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    list_collection = client.list_collections()
    return [collection.name for collection in list_collection]



def delete_collection(username:str, collection:str):
    """delete a spesific collection
    Args:
        username (str): To fetch User Directory 
        collection (str): to fetch collection
    Raises:
        Exception: Collection Not Found
        Exception: User Directory Not Found
    """
    persist_dir = DATABASE_PATH/username
    if persist_dir.exists():
        client = chromadb.PersistentClient(str(persist_dir.resolve()))
        try:
            client.delete_collection(collection)
        except Exception as e: 
            raise Exception("collection Not Found")
    else: raise Exception("User directory not found")
def get_answer(question:str,username:str, collection: str):
    """Make Query of the uploaded file 
    This function retrieve data from Vector store and pass through a prompt of llm model and retrieve answer. 

    Args:
        question (str): Question String 
        username (str): username for select user 
        collection (str): collection name for select collection 
    Return : 
        str : Answer String 
    """
    persist_dir = DATABASE_PATH/username
    if not persist_dir.exists():
        raise Exception(f"No directorr found as {username} ")
    client = chromadb.PersistentClient(str(persist_dir.resolve()))
    try:
        client.get_collection(collection)
    except:
        raise Exception(f"Collection {collection} not Found with this user {username}")

    chroma = Chroma(persist_directory=persist_dir.resolve().as_posix(), 
                     embedding_function=embedding_function,
                     collection_name=collection)
    ## Retrive content form Document 
    docs = chroma.similarity_search(question)
    print(docs)
    # # # Model Selection     
    # model_name = r'models/chat-bison-001'
    model_name = r'models/text-bison-001'
    # model_name = r'models/gemini-pro'
    # model_name = r'models//gemini-pro-version'
    # model_name = r'models/aqa'

    llm = GoogleGenerativeAI(model=model_name, google_api_key=GOOGLE_API_KEY)
    # llm.invoke("Hello how are you ?")

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