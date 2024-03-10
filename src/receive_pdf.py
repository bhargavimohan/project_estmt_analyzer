from fastapi import FastAPI,UploadFile, File
import random
import os
import asyncio
from review_pdf import main
from fastapi.responses import JSONResponse
from render_results import entry_exists_in_database

app = FastAPI()

# class FileHandler:
#     file_path = None

# file_handler = FileHandler()

@app.post("/receive")
async def receive_pdf_file(file: UploadFile = File(...)):
    with open(os.path.join("./pdfs", file.filename), "wb") as buffer:
        buffer.write(await file.read())
    estmnt_file_path = file.filename
    main(estmnt_file_path)
    is_analysis_complete = entry_exists_in_database(file.filename)
    if is_analysis_complete:
        return JSONResponse(content={"message": "Analysis completed"})
    else:
        return JSONResponse(content={"message": "Analysis incomplete"})

@app.get("/receive")
async def get_receive_page():
    return {"Info" : "Saving pdf and calculating costs..." }

    
# Add CORS middleware
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response