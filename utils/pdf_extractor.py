import PyPDF2
import io
import logging

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    
    Args:
        file_path (str or file-like object): Path to the PDF file or file-like object
    
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # If a string path is provided, open the file
        if isinstance(file_path, str):
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
    
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

def validate_pdf(file_path):
    """
    Validate if the file is a valid PDF.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        bool: True if valid PDF, False otherwise
    """
    try:
        with open(file_path, 'rb') as file:
            PyPDF2.PdfReader(file)
        return True
    except Exception:
        return False
