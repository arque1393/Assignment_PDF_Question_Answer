import os
import shutil 
from pathlib import Path

from fastapi import( FastAPI, File, UploadFile, HTTPException,Depends)
from _models import User,UserShow
from sqlalchemy.orm import Session
from db_setup import get_session, engine
import db_models

db_models.Base.metadata.create_all(engine)
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
        
app = FastAPI()
@app.post("/api/user/", response_model=UserShow)
async def create_user(usr:User, session:Session = Depends(get_session)):
    existing_object = session.query(db_models.User).filter_by(email=usr.email).first()
    if existing_object:
        raise HTTPException(status_code=400, detail='Email is already taken')    
    new_user = db_models.User(email = usr.email, _password = usr.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
    
@app.post("api/user/{user_id}/upload_pdf")
async def post_endpoint(user_id:int, in_file: UploadFile=File(...)):
    save_upload_file(in_file, Path('./tmp/tmp.pdf'))

    return {"Result": "OK"}