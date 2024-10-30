import os
from pdf2docx import Converter

def convert_pdf_to_docx(pdf_path, docx_path):
    # Create a PDF Converter object
    cv = Converter(pdf_path)  
    try:
        # Convert PDF to DOCX
        cv.convert(docx_path)
        print(f"Conversion complete. Output file: {docx_path}")
    except Exception as e:
        print(f"An error occurred during conversion: {str(e)}")
    finally:
        # Close the converter
        cv.close()

# Example usage
pdf_file = "input.pdf"
docx_file = "input.docx"

# Check if the input PDF file exists
if not os.path.exists(pdf_file):
    print(f"Error: The file '{pdf_file}' does not exist.")
else:
    convert_pdf_to_docx(pdf_file, docx_file)
