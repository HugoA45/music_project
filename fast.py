from fastapi import FastAPI, UploadFile
from main_2 import main

app = FastAPI()

# Define a root `/` endpoint
@app.post('/')
async def index(file: UploadFile):
    file_path = "upload.mp3"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return main(file_path, "fine_tuned")
