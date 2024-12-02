import os

def path():
# Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    return (current_directory + "\\OCR\\Tesseract-OCR\\tesseract.exe")

# print("Current directory of the file:", current_directory)

# from pathlib import Path

# # Get the directory of the current script
# current_directory = Path(__file__).parent

# print("Current directory of the file:", current_directory)
