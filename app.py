from flask import Flask, render_template, request, redirect, url_for
import os
import dotenv
from utils.pdf_extractor import extract_text_from_pdf, validate_pdf
from utils.image_extractor import extract_text_from_image, supported_image_formats
from utils.ai_processor import AIProcessor
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)

# Ensure upload directory exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load the saved model
model = load_model('chest_xray_model.h5')

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Initialize AI Processor
ai_processor = AIProcessor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/blood_report_analyzer", methods=["GET", "POST"])
def blood_report_analyzer():
    summary = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file:
            # Get file extension
            file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # Save the uploaded file
            uploaded_file.save(file_path)
            
            try:
                # Extract text based on file type
                if file_ext == '.pdf':
                    # Validate and extract from PDF
                    if validate_pdf(file_path):
                        extracted_text = extract_text_from_pdf(file_path)
                    else:
                        summary = "Invalid PDF file. Please upload a valid PDF."
                        return render_template("blood_report_analyzer.html", summary=summary)
                
                elif file_ext in supported_image_formats():
                    # Extract text from image
                    extracted_text = extract_text_from_image(file_path)
                
                else:
                    summary = f"Unsupported file type: {file_ext}. Please upload a PDF or image."
                    return render_template("blood_report_analyzer.html", summary=summary)
                
                # Validate if the document seems to be medical
                if ai_processor.validate_medical_document(extracted_text):
                    # Summarize the report
                    summary = ai_processor.summarize_medical_document(extracted_text)
                else:
                    summary = "The uploaded document does not appear to be a medical report."
            
            except Exception as e:
                summary = f"Error processing document: {str(e)}"
            
            finally:
                # Remove the uploaded file after processing
                os.remove(file_path)
    
    return render_template("blood_report_analyzer.html", summary=summary)

@app.route('/x_ray_analyzer',methods=["GET", "POST"])
def x_ray_analyzer():
    summary = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file:
            # Get file extension
            file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # Save the uploaded file
            uploaded_file.save(file_path)
            
            try:
                # Preprocess the image
                img_array = preprocess_image(file_path)
                # Make prediction
                prediction = model.predict(img_array)
                if prediction[0][0] > 0.5:
                    summary = "The X-ray indicates pneumonia."
                else:
                    summary = "The X-ray does not indicate pneumonia."
            
            except Exception as e:
                summary = f"Error processing image: {str(e)}"
            
            finally:
                os.remove(file_path)
                summary = ai_processor.summarize_x_ray(f"Generate a short summary on {summary} (Probability: {prediction[0][0]})")

    return render_template('x_ray_analyzer.html', summary=summary)

@app.route('/ecg_analyzer')
def ecg_analyzer():
    return render_template('ecg_analyzer.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
