Introduction

  This API provides Optical Character Recognition (OCR) functionality, 
  allowing users to upload image or PDF files for text extraction. 
  Additionally, the API detects tables in PDF files and returns them in a structured format. 
  It is built using FastAPI, pytesseract for OCR, and pdfplumber for PDF table detection.

Features

   Image OCR: Extracts text from images (JPEG, PNG, etc.).
   PDF OCR: Extracts text from PDF files and detects tables.
   Table Detection: Detects and processes tables from PDF files into structured data.
   
Prerequisites

    Tesseract OCR: You need to install Tesseract for OCR functionality.
    Download from: Tesseract OCR Download
       Set the path to the environment variable.
       like:- C:\Program Files\Tesseract-OCR

    Poppler: Required for converting PDFs to images.
    Download from: Poppler Download
       Set the path to the environment variable.
       like:- C:\poppler\Library\bin
       
Python Dependencies: Install the following Python packages:
   pip install fastapi uvicorn pytesseract pdf2image pdfplumber pandas Pillow

How to run 
   - run using this command in the main directory
        uvicorn main:app --reload
How to test 
   - test using this endpoint in the browser
      http://127.0.0.1:8000/docs

Contact
  - For any help or questions, please don't hesitate to reach out. 
    I'm here to assist you and would be happy to provide the support you need!
    phone: +251923233128
    
    email: yilkalderseh@gmail.com
