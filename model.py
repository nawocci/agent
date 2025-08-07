import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiModel:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        print("✅ Successfully connected to Gemini API")
    
    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def chat(self, message: str) -> str:
        try:
            chat = self.model.start_chat()
            response = chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error in chat: {str(e)}"