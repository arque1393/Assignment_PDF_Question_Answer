from pydantic import BaseModel
class User(BaseModel):
    password: str
    username: str

class UserShow(BaseModel):
    username:str
    user_id:int
  
class UploadInfo(BaseModel):
    file_name:str
    collection_name:str|None
    
class AskInfo(BaseModel):
    collection_name: str
    question:str