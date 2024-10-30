import boto3
import fitz  # PyMuPDF
from botocore.exceptions import ClientError
import argparse

def parse_arguments():
    """
    Parse command line arguments for PDF translation.
    Returns:
        argparse.Namespace: Parsed command line arguments containing:
            - input_file: Path to source PDF
            - output_file: Path for translated PDF
            - source_lang: Source language code
            - target_lang: Target language code
    """
    parser = argparse.ArgumentParser(description='Translate PDF document from one language to another.')
    parser.add_argument('input_file', help='Path to the input PDF file')
    parser.add_argument('output_file', help='Path for the translated PDF file')
    parser.add_argument('--source-lang', default='en', help='Source language code (default: en)')
    parser.add_argument('--target-lang', default='es', help='Target language code (default: es)')
    return parser.parse_args()

def translate_text(text, source_lang='en', target_lang='es'):
    """
    Translate text using AWS Translate service.
    Args:
        text (str): Text to translate
        source_lang (str): Source language code (default: 'en')
        target_lang (str): Target language code (default: 'es')
    Returns:
        str: Translated text, or original text if translation fails
    """
    try:
        translate = boto3.client('translate')
        response = translate.translate_text(
            Text=text,
            TerminologyNames=['vsp'],
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang,
            Settings={
                "Formality": "FORMAL"
            }
        )
        return response['TranslatedText']
    except ClientError as e:
        print(f'Error translating text: {e}')
        return text

def main():
    """
    Main function to handle PDF translation workflow:
    1. Extract text and layout from PDF
    2. Translate extracted text
    3. Generate new PDF with translated text
    """
        
    # Parse command line arguments
    args = parse_arguments()

    # Step 1: Extract text and layout using PyMuPDF
    pdf_document = fitz.open(args.input_file)
    text_blocks = []

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:  # Type 0 is text
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_blocks.append({
                            "text": span["text"],
                            "bbox": span["bbox"],
                            "font_size": span["size"],
                            "font_name": span["font"],
                            "page_num": page_num
                        })

    # Step 2: Translate text
    for block in text_blocks:
        block["translated_text"] = translate_text(
            block["text"],
            source_lang=args.source_lang,
            target_lang=args.target_lang
        )

    # Step 3: Replace text in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        for block in text_blocks:
            if block["page_num"] == page_num:
                rect = fitz.Rect(block["bbox"])
                
                # Remove the original text
                page.add_redact_annot(rect)
                page.apply_redactions()
                
                try:
                    # Try to insert text with original font
                    page.insert_text(
                        rect.tl,
                        block["translated_text"],
                        fontsize=block["font_size"],
                        fontname=block["font_name"],
                        color=(0, 0, 0)
                    )
                except Exception as e:
                    # Fallback to a default font
                    page.insert_text(
                        rect.tl,
                        block["translated_text"],
                        fontsize=block["font_size"],
                        fontname="helv",  # Using Helvetica as a fallback
                        color=(0, 0, 0)
                    )

    pdf_document.save(args.output_file)
    pdf_document.close()
    print(f'Translated PDF saved to {args.output_file}')

if __name__ == '__main__':
    main()
