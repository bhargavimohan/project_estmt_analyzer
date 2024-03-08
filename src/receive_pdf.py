from fastapi import FastAPI,UploadFile, File
import random
import os

app = FastAPI()


@app.post("/receive")
async def receive_pdf_file(file: UploadFile = File(...)):
    with open(os.path.join("./pdfs", file.filename), "wb") as buffer:
        buffer.write(await file.read())
    return {"filename": file.filename}

@app.get("/receive")
async def get_receive_page():
    return {"Info" : "Saving pdf and calculating costs..." }

# Add CORS middleware
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response