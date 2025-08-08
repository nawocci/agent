import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiModel:
    def __init__(self, system_prompt: str = ""):
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        self.system_prompt = system_prompt
        # Use system_instruction so we don't prepend the prompt each turn
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=self.system_prompt or None,
        )
        
        print("✅ Successfully connected to Gemini API")
    
    def generate_text(self, prompt: str) -> str:
        try:
            # System prompt already set via system_instruction
            response = self.model.generate_content(prompt)
            # Be defensive in case text is None
            return response.text or ""
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def chat(self, message: str) -> str:
        try:
            chat = self.model.start_chat()
            response = chat.send_message(message)
            return response.text or ""
        except Exception as e:
            return f"Error in chat: {str(e)}"