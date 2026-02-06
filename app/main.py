from fastapi import FastAPI, UploadFile, File
import os
import tempfile

from app.extractor import extract_fields_with_ai
from app.router import detect_missing, route_claim
from app.utils import load_document

app = FastAPI(title="AI Claims Processing Agent")

@app.post("/process-claim")
async def process_claim(file: UploadFile = File(...)):
    # Get file extension
    _, ext = os.path.splitext(file.filename)

    # Save uploaded file temporarily with correct extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Read document
    text = load_document(tmp_path)

    # Extract fields with AI
    fields = extract_fields_with_ai(text)

    # Detect missing fields
    missing = detect_missing(fields)

    # Route claim
    route, reason = route_claim(fields, missing)

    # Remove temp file
    os.remove(tmp_path)

    return {
        "extractedFields": fields,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": reason
    }
