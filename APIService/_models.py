from pydantic import BaseModel

class FileInfo(BaseModel):
    filename:str
    file_path:str
    
class AskInfo(BaseModel):
    pdf_name: str
    question:str