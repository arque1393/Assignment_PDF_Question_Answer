from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
import shutil 
from pathlib import Path

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
        
app = FastAPI()
@app.post("/")
async def post_endpoint(in_file: UploadFile=File(...)):
    save_upload_file(in_file, Path('./tmp/tmp.pdf'))

    return {"Result": "OK"}