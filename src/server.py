from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
from review_pdf import process_pdf
from fastapi.middleware.cors import CORSMiddleware
from db_manager import (
    entry_exists_in_database,
    get_analyzed_pdf_from_db,
    delete_pdf_entry_from_db,
    get_analyzed_pdfs_list_from_db,
)

app = FastAPI()

pdfs_path = Path("./pdfs")
pdfs_path.mkdir(exist_ok=True)


# Add CORS middleware
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return JSONResponse(content={"message": "Running PDF Analyzer"})


@app.post("/receive")
async def receive_pdf_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=422, detail="Invalid file type. Only PDF files are allowed."
        )
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
        return JSONResponse(
            content={"message": "File received and analysis may have been completed"}
        )
    else:
        return JSONResponse(
            content={"message": "File not received or analysis incomplete"},
            status_code=202,
        )


@app.get("/analyzed-pdfs")
async def get_analyzed_pdfs_list(
    year: int = Query(None, description="Filter results by year")
):
    try:
        items = get_analyzed_pdfs_list_from_db(year)
        if len(items) == 0:
            return JSONResponse(content={"message": "No PDFs analyzed yet!"})
        return {"items": items}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve analyzed PDFs: {e}"
        )


@app.get("/analyze/{pdf_name}")
def get_analyzed_pdf(pdf_name: str):
    try:
        analysis = get_analyzed_pdf_from_db(pdf_name)
        if analysis:
            return JSONResponse(content=analysis)
        else:
            return JSONResponse(status_code=404, content={"message": "File not found"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analysis: {e}")


@app.delete("/delete/{pdf_name}")
def delete_pdf_entry(pdf_name: str):
    try:
        if delete_pdf_entry_from_db(pdf_name):
            return {"message": f"File {pdf_name} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {e}")
