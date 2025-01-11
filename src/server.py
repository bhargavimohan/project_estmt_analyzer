from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
import os
from review_pdf import process_pdf
from db_manager import entry_exists_in_database
from models import Results, Session


app = FastAPI()

pdfs_path = Path("./pdfs")
pdfs_path.mkdir(exist_ok=True)


@app.post("/receive")
async def receive_pdf_file(file: UploadFile = File(...)):
    file_path = pdfs_path / file.filename
    try:
        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to save file: {e}"
        )  # copy the content of the uploaded file to a new file on local.
    try:
        process_pdf(file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")

    is_analysis_complete = entry_exists_in_database(file.filename)
    if is_analysis_complete:
        return JSONResponse(content={"message": "Analysis completed"})
    else:
        return JSONResponse(content={"message": "Analysis incomplete"})


@app.get("/analyzed-pdfs")
async def get_analyzed_pdfs_list():
    items = [
        {item.file_name: item.output_json} for item in Session.query(Results).all()
    ]
    return {"items": items}


# Add CORS middleware
@app.middleware("http")
async def add_cors_header(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
