# PDF Language Translator

A Python tool that translates PDF documents while preserving their original layout and formatting. The tool uses AWS Translate for high-quality translations and maintains the original document's structure, fonts, and positioning.

## Features

- Preserves original PDF layout and formatting
- Supports multiple language pairs for translation
- Maintains original font sizes and positioning
- Falls back to Helvetica font if original fonts are unavailable
- Uses AWS Translate with formal translation settings
- Supports custom terminology through AWS Translate terminology sets

## Prerequisites

- Python 3.x
- AWS account with appropriate credentials configured
- Required Python packages:
  - boto3
  - PyMuPDF (fitz)
  - botocore

## Installation

1. Clone the repository
2. Install required packages:
```pip install boto3 PyMuPDF```
3. Configure AWS credentials

## Usage

```bash
# Basic usage (English to Spanish)
python translate_pdf.py input.pdf output.pdf

# Specify source and target languages
python translate_pdf.py input.pdf output.pdf --source-lang en --target-lang fr
