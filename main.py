from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.openapi.models import APIKey
from typing import List, Dict, Any
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import pdfplumber  # Added for PDF table detection
import pandas as pd  # Added for structured table data handling

# Set the path to the Tesseract executable if it's not automatically detected
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path = r'C:\poppler\Library\bin'  # Adjust the path based on where you installed Poppler

app = FastAPI(
    title="OCR Service API",
    description="This API allows users to upload images or PDF files for Optical Character Recognition (OCR), including table detection.",
    version="1.1.0",
    contact={
        "name": "OCR Service",
        "email": "support@ocrservice.com"
    }
)

# Root endpoint
@app.get("/", summary="Welcome Endpoint", description="Root endpoint to welcome users to the OCR service.")
async def root():
    return {"message": "Welcome to the OCR Service. Use the /ocr endpoint to upload a file for OCR."}

# OCR function to extract text from an image
def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

# OCR function to extract text from a PDF
def extract_text_from_pdf(pdf_file: bytes) -> str:
    images = convert_from_bytes(pdf_file, poppler_path=poppler_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

# Function to detect tables in a PDF using pdfplumber
def extract_tables_from_pdf(pdf_file: bytes) -> List[Dict[str, Any]]:
    tables = []
    with pdfplumber.open(io.BytesIO(pdf_file)) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                # Convert table to a more structured format using pandas
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df.to_dict(orient="records"))
    return tables

# API endpoint to handle OCR with table detection
@app.post(
    "/ocr",
    summary="OCR Service Endpoint with Table Detection",
    description="Upload an image or a PDF file for OCR processing with table detection. Returns the extracted text and any detected tables from the uploaded file.",
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "example": {
                        "extracted_text": "Sample extracted text",
                        "tables": [
                            [{"Column1": "Value1", "Column2": "Value2"}, {"Column1": "Value3", "Column2": "Value4"}]
                        ]
                    }
                }
            }
        },
        400: {"description": "Unsupported file type"},
        500: {"description": "Internal server error"}
    }
)
async def ocr_service(file: UploadFile = File(...)):
    """
    Perform OCR on the uploaded file.

    - **file**: Upload an image file (JPEG, PNG, etc.) or a PDF file.
    - The service will extract text and tables (if any) from the file and return them in the response.
    """
    extracted_text = ""
    tables = []

    if file.content_type.startswith('image/'):
        try:
            # Read the image file
            image = Image.open(io.BytesIO(await file.read()))
            # Extract text from the image
            extracted_text = extract_text_from_image(image)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    elif file.content_type == 'application/pdf':
        try:
            # Read the PDF file
            pdf_bytes = await file.read()
            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_bytes)
            # Detect tables from the PDF
            tables = extract_tables_from_pdf(pdf_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    return JSONResponse(content={"extracted_text": extracted_text, "tables": tables})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
