#%% 
import os
from pathlib import Path
## Define Directory Constant 
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR/'ChromaDB'
FILE_STORE = BASE_DIR/'FileStore'

## Google API key 
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

## User Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./user.db"