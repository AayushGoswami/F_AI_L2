# __F_AI_L2__
## Flaunch AI Internship Level 2 Project

### Follow these steps to run this repository:

  - In your terminal, run the following code: `pip install -r requirements.txt`
    
  - To run this website, clone the repository and then edit the  ___.env___ file.
    `GROQ_API_KEY=your_original_groq_api_key`
    In this file, replace the placeholder `your_own_groq_api_key` with your actual __GROQ API KEY__.
  
  - If you do not have __Tesseract-OCR__ installed in your device, download the __`tesseract-ocr-w64-setup-5.5.0.20241111.exe`__ and install it in your device. If you have it already installed in your device, then no need to do this step.
  
  - Copy the file path of the __TESSERACT-OCR__ folder and add it in the `utils/image_extractor.py` file.
    in the 7th line of the file, `pytesseract.pytesseract.tesseract_cmd = r"your_TESSERACT-OCR_folder_path\tesseract.exe"`, replace the `your_TESSERACT-OCR_folder_path` part with your actual __TESSERACT-OCR__ folder.


## __You are ready to run the project 😊__
