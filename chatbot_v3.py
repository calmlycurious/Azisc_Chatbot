from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are Azisc, a friendly and intelligent AI assistant created by Ashish Gurung, a BCA second year student from Siliguri, West Bengal, India, who is passionate about AI and Machine Learning.

Your personality:
- Friendly, encouraging and approachable
- You explain things clearly and simply
- You love talking about technology, AI and programming
- You always motivate students to keep learning
- You keep responses concise and to the point
- If someone asks who made you, say "I was built by Ashish Gurung!"

You are here to help users with questions, learning and general coversation.
"""

def get_ai_response(chat_history):
    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = chat_history,
        config = types.GenerateContentConfig(
            system_instruction = SYSTEM_PROMPT
        )
    )
    return response.text

def add_message(chat_history, role, text):
    chat_history.append({
        "role": role,
        "parts": [{"text": text}]
    })
    
def main():
    print("=" * 45)
    print(" Welcome to Azisc - Your AI Assistant")
    print(" Created by Ashish Gurung | Type 'quit' to exit.")
    print("=" * 45)
    
    chat_history = []
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            print("Azisc: Please type something!")
            continue
        
        if user_input.lower() == "quit":
            print("Azisc: Goodbye! Keep learning and stay awesome!")
            break
        
        add_message(chat_history, "user", user_input)
        
        print("Azisc: Thinking....")
        reply = get_ai_response(chat_history)
        print(f"\nAzisc: {reply}")
        
        add_message(chat_history, "model", reply)
        
if __name__ == "__main__":
    main()   