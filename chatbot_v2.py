from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_ai_response(chat_history):
    response = client.models.generate_content(
        model = "gemini-2.5-flash-lite",
        contents = chat_history
    )
    return response.text

def add_message(chat_history, role, text):
    chat_history.append({
        "role": role,
        "parts": [{"text": text}]
    })

def main():
    print("=" * 45)
    print("     Welcome to Azisc - Your AI Assistant")
    print("     Type 'quit' to exit")
    print("=" * 45)
    
    chat_history = []
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            print("Azisc: Please stop typing!")
            continue
        
        if user_input.lower() == "quit":
            print("Azisc: Goodbye! Have a great day.")
            break
            
        add_message(chat_history, "user", user_input)
        
        print("Azisc: Thinking...")
        reply = get_ai_response(chat_history)
        print(f"Azsic: {reply}")
        
        add_message(chat_history, "model", reply)
        
if __name__ == "__main__":
    main()