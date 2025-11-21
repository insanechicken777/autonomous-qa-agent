import os
import shutil
from fastapi import FastAPI, UploadFile, File
from typing import List
from .rag_utils import build_knowledge_base # Import our logic function
from fastapi import Form
from .rag_utils import generate_test_cases, generate_selenium_script # Update import

app = FastAPI()

# Create a temporary folder to store uploaded files
UPLOAD_DIR = "./temp_uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "QA Agent Backend is Running!"}

@app.post("/upload-documents/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Receives a list of files, saves them locally, 
    and triggers the Vector DB build.
    """
    # 1. Clear old uploads to keep things clean
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        os.remove(file_path)

    # 2. Save new files
    saved_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            # Read the uploaded file and write it to disk
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

    # 3. Build the Knowledge Base (Call the function from rag_utils)
    result = build_knowledge_base(UPLOAD_DIR)

    return {
        "message": "Files uploaded and Knowledge Base Built successfully",
        "files": saved_files,
        "db_status": result
    }

@app.post("/generate-tests/")
async def generate_tests_endpoint(query: str = Form(...)):
    """
    Example query: "Generate positive and negative tests for the discount code."
    """
    result = generate_test_cases(query)
    return {"test_cases": result}

@app.post("/generate-script/")
async def generate_script_endpoint(test_case_json: str = Form(...), html_content: str = Form(...)):
    """
    Takes a specific test case and the HTML string, returns Python code.
    """
    script = generate_selenium_script(test_case_json, html_content)
    return {"script": script}