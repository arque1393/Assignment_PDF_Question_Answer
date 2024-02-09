#%% 
import os
from pathlib import Path
## Define Directory Constant 
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR/'ChromaDB'

## Google API key 
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

