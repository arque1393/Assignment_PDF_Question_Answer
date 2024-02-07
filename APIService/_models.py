from pydantic import BaseModel
class User(BaseModel):
    username: str
    password: str

class UserShow(BaseModel):
    username:str
    user_id:int
    class Config:
        orm_mode = True
class UploadInfo(BaseModel):
    file_name:str
    collection_name:str|None
    
class AskInfo(BaseModel):
    collection_name: str
    question:str