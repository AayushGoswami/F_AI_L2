import os
import logging
from typing import Optional, List
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
class AIProcessor:
    
    def __init__(self):
        
        # Use provided API key or try to get from environment
        api_key = os.environ.get('GROQ_API_KEY')
        
        if not api_key:
            raise ValueError("No Groq API key provided. Set GROQ_API_KEY environment variable.")
        
        # Initialize the Groq client
        self.client = Groq(api_key=api_key)
    
    def summarize_medical_document(
        self, 
        text: str,
    ) -> str:

        try:
            # Validate input
            if not text or len(text.strip()) < 10:
                return "Insufficient text for meaningful analysis."
            
            # Construct prompt
            prompt = f"""Analyze and summarize the following medical document. 
            Provide a clear, concise summary highlighting key medical insights, 
            important parameters, and any potential areas of concern:

            {text}
                    """
            
            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                        }
                ],
                model="llama-3.2-11b-vision-preview",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"
    
    def summarize_x_ray(self, text: str,) -> str:

        try:
            # Construct prompt
            prompt = f"""Analyze and summarize the following X-ray report in 3-4 lines.{text}"""
            
            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                        }
                ],
                model="llama-3.2-11b-vision-preview",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"

    def analyze_medical_parameters(
        self, 
        text: str, 
        parameters: Optional[List[str]] = None
    ) -> dict:

        try:
            # Default parameters if none provided
            if not parameters:
                parameters = [
                    'hemoglobin', 'white blood cell count', 'platelets', 
                    'red blood cell count', 'blood glucose', 'cholesterol'
                ]
            
            # Construct prompt
            prompt = f"""From the following medical document, extract the values 
            for these specific parameters: {', '.join(parameters)}

            Document:
            {text}

            Provide the output in a clear JSON-like format with parameter names as keys 
            and their values. If a parameter is not found, use null."""
            
            # Generate response
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",  # Using the smaller 8b model for this task
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300
            )
            # Extract and return the parameter analysis
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logging.error(f"Error in parameter extraction: {e}")
            return {"error": str(e)}

    @staticmethod
    def validate_medical_document(text: str) -> bool:
        """
        Basic validation of whether the text appears to be a medical document.
        
        Args:
            text (str): Text to validate
        
        Returns:
            bool: Whether the text seems to be a medical document
        """
        medical_keywords = [
            'patient', 'report', 'blood', 'test', 'result', 
            'medical', 'diagnosis', 'laboratory', 'clinic'
        ]
        
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check if sufficient medical keywords are present
        keyword_count = sum(1 for keyword in medical_keywords if keyword in text_lower)
        
        return keyword_count >= 3
