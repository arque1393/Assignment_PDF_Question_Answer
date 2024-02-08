## Problem Statement 
**Overview**: In this assignment, you will create a Question and Answer (Q&A) application that utilizes LangChain, Google PaLM 2, and the Chroma Vector Database to extract information from private PDF documents. The assignment is designed to deepen your understanding of these technologies while fostering hands-on experiences.

## API KEY Setup in Windows 
setx OPENAI_API_KEY "< valure >"<br>
setx GOOGLE_API_KEY "< value >"

## Video Description link
https://1drv.ms/f/s!Aj2Nbw_0FL8Hia4YoiaxorZi_elkzA?e=FVpEix

## Solution Approach 
My Approach is very simple I use ChromaDB database to store Documents as form of vectors. and according to the question I retrieve  the relevant context and pass through the llm chain to find appropriate answer of the question. I use langchain LLMChain and Prompt Template to implement all those things.
Finally Integrate all with the FastAPI App and create a backend app 

### Steps : 
    Storing PDF content in  Database
        1. Parse PDF document and retrieve content page by page 
        2. Divide pages into smaller chunks and store as list of documents.
        3. Search Embedding Models 
        4. Create specific collection in main ChromaDB database.
        5. From document list add all content to the collections
    Retrieve content from Database 
        1. Load content from ChromaDB Database
        2. Perform Similarity search to retrieve  relevant content.
    LLM Prediction :
        1. Define a proper Prompt Template with variable _Knowledge_ and _Question_
        2. calling llm to get answer 

### Fast API end points :
      POST : http:/localhost/api/user
        Create User 

      POST : http:/localhost/api/user/{user_id}/upload_pdf
        upload PDF file for specific user

      POST : http:/localhost/api/user/{user_id}/store
        Store PDF file content in collection

       GET : http:/localhost/api/user/{user_id}/collections
        get list of collection name for specific user 

    DELETE : http:/localhost/api/user/{user_id}/{collection}
        Delete Specific collection for specific 

      POST : http:/localhost/api/user/{user_id}/collections
        Ask question from specific collection for specific user 

### Models I explored 
- Embedding Models 
    - sentence-transformers/all-MiniLM-L6-v2  (sentence-transformers)
    - models/embedding-gecko-001 (Google)
    - models/embedding-001 (Google)
- Text Generation 
    - models/chat-bison-001   (Google)
    - models/text-bison-001   (Google)
    - models/gemini-pro    (Google)
    - models/aqa        (Google)


