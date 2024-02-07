import os
import shutil 
from pathlib import Path

from fastapi import( FastAPI, File, UploadFile, HTTPException,Depends)
from _models import User,UserShow,UploadInfo,AskInfo
from sqlalchemy.orm import Session
from db_setup import get_session, engine
import db_models
from config import DATABASE_PATH, FILE_STORE_PATH

from vector_store import upload_on_vector_db, get_answer,get_collection_list

db_models.Base.metadata.create_all(engine)
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
        
app = FastAPI()
@app.post("/api/user", response_model=UserShow)
async def create_user(usr:User, session:Session = Depends(get_session)):
    existing_object = session.query(db_models.User).filter_by(username=usr.username).first()
    if existing_object:
        raise HTTPException(status_code=400, detail='Username is already taken')    
    new_user = db_models.User(username = usr.username, _password = usr.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    print(new_user)
    return new_user
    
@app.post("/api/user/{user_id}/upload_pdf")
async def post_endpoint(user_id:int, session:Session=Depends(get_session), in_file: UploadFile=File(...)):
    file_name=in_file.filename
    user = session.query(db_models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')    
        
    user_name = user.username
    dir_location =  FILE_STORE_PATH/user_name
    if not dir_location.exists():
        dir_location.mkdir(parents=True)
    save_upload_file(in_file, dir_location/file_name)
    
    return {"Result": "OK"}

@app.post("/api/user/{user_id}/store")
async def add_on_vector_db(user_id:int, upload_info:UploadInfo,
                    session:Session = Depends(get_session)):
    user =  session.query(db_models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')  
    user_name = user.username
    try:
        if not upload_info.collection_name:
            upload_info.collection_name='default'
        upload_on_vector_db(username=user_name,file_name=upload_info.file_name,collection_name=upload_info.collection_name)
    except Exception as e:
        raise HTTPException(e)
@app.get("/api/user/{user_id}/collections")
async def get_all_collections(user_id:int,session:Session = Depends(get_session)):
    user =  session.query(db_models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')  
    user_name = user.username
    return get_collection_list(user_name)

@app.post("/api/user/{user_id}/ask/")
async def ask_question(user_id:int, ask_info:AskInfo,
                    session:Session = Depends(get_session)) :
    user =  session.query(db_models.User).filter_by(user_id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')  
    user_name = user.username
    if not ask_info.collection_name:
        ask_info.collection_name='default'
    try:
        answer = get_answer(question=ask_info.question, username=user_name, collection=ask_info.collection_name)
        return {'question':ask_info.question, 'answer':answer}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))