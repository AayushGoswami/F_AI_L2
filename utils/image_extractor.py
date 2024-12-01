import pytesseract
from PIL import Image
import cv2
import numpy as np
import logging

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        numpy.ndarray: Preprocessed image
    """
    try:
        # Read the image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Apply deskewing
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        # The cv2.minAreaRect returns values in the range [90, -90)
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Rotate the image to deskew it
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None

def extract_text_from_image(image_path, lang='eng'):
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file
        lang (str, optional): Language for OCR. Defaults to 'eng'.
    
    Returns:
        str: Extracted text from the image
    """
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)
        
        if preprocessed_image is None:
            logging.error("Image preprocessing failed")
            return ""
        
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(preprocessed_image, lang=lang)
        
        return text.strip()
    
    except Exception as e:
        logging.error(f"Error extracting text from image: {e}")
        return ""

def supported_image_formats():
    """
    List of supported image formats for OCR.
    
    Returns:
        list: Supported image file extensions
    """
    return ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']