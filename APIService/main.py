from pathlib import Path

from fastapi import FastAPI, HTTPException
from _models import FileInfo, AskInfo
from vector_store import upload_on_vector_db, get_answer
# Creating or updating table structure on User Database
app = FastAPI()
@app.get("/")
async def root():
    return {"message":"Check Docs for test API"}
@app.post("/api/upload_pdf")
async def add_PDF( file_info : FileInfo):
    file_name=file_info.filename
    file_path=Path(file_info.file_path)
    if not file_path.exists():
        raise HTTPException("File Path does not exist")
    try:     
        upload_on_vector_db(file_path=file_path/file_name,
                            collection_name=file_name[0:-4])
        return {'status':'success'}
    except Exception as e:
        raise HTTPException(status_code=409,detail=str(e))
    
@app.post("/ask/pdf")
async def ask_question( ask_info:AskInfo) :   
    try:
        answer = get_answer(question=ask_info.question,  collection=ask_info.pdf_name[0:-4])
        return {'question':ask_info.question, 'answer':answer}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    
    
    
    
    