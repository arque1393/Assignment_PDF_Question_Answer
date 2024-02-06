from pydantic import BaseModel, EmailStr
class User(BaseModel):
    password: str
    email: EmailStr

class UserShow(BaseModel):
    email:EmailStr
    user_id:int
  