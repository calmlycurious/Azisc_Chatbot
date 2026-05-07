from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .ennv file!")
    print("Please add your API key to the .env file and try again.")
    exit()
    
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are Azisc, a friendly and intelligent AI assistant created
by Ashish Gurung, a BCA second year student from Siliguri, West Bengal, India, who is
passionate about AI and Machine Learning.

Your personality:
- Friendly, encouraging and approachable
- You explain things clearly and simply
- You love talking about technology, AI and programming
- You always motivate students to keep learning
- You keep responses concise and to the point
- If someone asks who made you, say "I was built by Ashish Gurung!"
"""

def get_ai_response(chat_history):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=chat_history,
            config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )
        return response.text

    except Exception as e:
        error_message = str(e)
        
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            print("\nAzisc: I am getting too many requests right now.")
            print("Azisc: Waiting 30 seconds and trying again...\n")
            time.sleep(30)
            try:
                response = client.models.generate_content(
                    model = "gemini-2.5-flash-lite",
                    contents = chat_history,
                    config = types.GenerateContentConfig(
                        system_instruction = SYSTEM_PROMPT
                    )
                )
                return response.text
            except Exception:
                return "Still hitting rate limits. Please wait a minute before trying again."
            
        elif "403" in error_message or "PERMISSION_DENIED" in error_message:
            return "No internet connection. Please check your network and try again."
        
        else:
            return f"Something went wrong: {error_message[:100]}"
        
def add_message(chat_history, role, text):
    chat_history.append({
        "role": role,
        "parts": [{"text": text}]
    })

def show_help():
    print("\n" + "=" * 45)
    print("       Azisc — Available Commands")
    print("=" * 45)
    print("  /help      Show this help message")
    print("  /clear     Clear conversation memory")
    print("  /history   Show conversation history")
    print("  quit       Exit the chatbot")
    print("=" * 45 + "\n")

def show_history(chat_history):
    
    if not chat_history:
        print("\nAzisc: No conversation history yet!\n")
        return
    
    print("\n" + "=" * 45)
    print("        Conversation History")
    print("=" * 45)
    
    for message in chat_history:
        role = message["role"]
        text = message["parts"][0]["text"]
        
        if role == "user":
            print(f"\n  You   : {text}")
        
        else:
            print(f"  Azisc : {text}")
    print("\n" + "=" * 45 + "\n")

def handle_command(command, chat_history):
    command = command.lower().strip()
    
    if command == "/help":
        show_help()
    
    elif command == "/clear":
        chat_history.clear()
        print("\nAzisc: Memory cleared! Fresh start.\n")
    
    elif command == "/history":
        show_history(chat_history)
    
    else:
        print(f"\nAzisc: Unknown command '{command}'. Type /help to see commands.\n")

def main():
    print("=" * 45)
    print("     Welcome to Azisc — Your AI Assistant")
    print("  Created by Ashish | Type /help for commands")
    print("=" * 45)

    chat_history = []
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except KeyboardInterrupt:
            print("\n\nAzisc: Caught a Ctrl+C! Goodbye!")
            break
        
        if not user_input:
            print("Azisc: Please type something!")
            continue
        if user_input.lower() == "quit":
            print("Azisc: Goodbye! Keep learning and stay awesome!")
            break

        if user_input.startswith("/"):
            handle_command(user_input, chat_history)
            continue

        add_message(chat_history, "user", user_input)
        print("Azisc: Thinking...")
        reply = get_ai_response(chat_history)
        print(f"\nAzisc: {reply}")
        add_message(chat_history, "model", reply)

if __name__ == "__main__":
    main()