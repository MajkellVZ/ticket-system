import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def run_gemini_prompt(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text