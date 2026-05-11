"""
Azisc - AI Chatbot
===================
A Conversational AI chatbot using Google's Gemini API. Created by Ashish Gurung | BCA 2nd Year student | Siliguri.

Features:
- Multi- turn conversation with memory
- Custom AI persona via system prompt
- Slash commands (/help, /clear, /history)
- Graceful error handling
- Clean, modular code structure
"""

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

# Constants
MODEL_NAME = "gemini-2.5-flash-lite"
RETRY_WAIT_SECONDS = 30
BOT_NAME = "Azisc"
CREATOR_NAME = "Ashish Gurung"

# Persona
SYSTEM_PROMPT = f"""
You are {BOT_NAME}, a friendly and intelligent AI assistant created by {CREATOR_NAME}, a  BCA second year student from Siliguri, West Bengal, India who is passionate about AI and Machine Learning.

Your personality:
- Friendly, encouraging and approachable
- You explain things clearly and simply
- You love talking about technology, AI and programming
- You always motivate students to keep learning
- You keep responses concise and to the point

When someone asks "who are you" or "what are you":
- Say "I am {BOT_NAME}, your friendly AI Assistant! I am here to help you with questions, learning and general conversation."

When someone asks "who made you" or "who built you" or "who created you":
- Say "I was built by {CREATOR_NAME}, a BCA student from Siliguri!"
"""

def initialise_client() -> genai.Client:
    """
    Loads the API key from .env and initialises the Gemini client.
    
    Returns:
        genai.Client: Authenticated Gemini client
        
    Raises:
        SystemExit: If API key is missing
    """
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file!")
        print("Please add your API key and try again.")
        exit()
        
    return genai.Client(api_key=api_key)
    
# Core Functions
def add_message(chat_history: list, role: str, text: str) -> None:
        """
        Appends a new message to the conversation history.
        
        Args:
            chat_history (list): The running conversation history
            role (str): Either 'user' or 'model'
            text (str): The message content
        """
        chat_history.append({
            "role" : role,
            "parts" : [{"text": text}]   
        })
        
def get_ai_response(client: genai.Client, chat_history: list) -> str:
    """
    Sends the full conversation history to Gemini and returns the reply. Automatically retires once on rate limit errors.
    
    Args:
        client (genai.Client): The authenticated Gemini client
        chat_history (list): Full conversation history
        
    Returns:
        str: The AI's response text or an error message
    """ 
    try:
        response = client.models.generate_content(
            model = MODEL_NAME,
            contents = chat_history,
            config = types.GenerateContentConfig(
                system_instruction = SYSTEM_PROMPT
            )
        )
        return response.text
    
    except Exception as e:
        error_message = str(e)
        
        # Rate limit - wait and retry once
        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            print(f"\n{BOT_NAME}: Rate limit hit. Waiting {RETRY_WAIT_SECONDS}...\n")
            time.sleep(RETRY_WAIT_SECONDS)
            try:
                response = client.models.generate_content(
                    model = MODEL_NAME,
                    contents = chat_history,
                    config = types.GenerateContentConfig(
                        system_instruction = SYSTEM_PROMPT
                    )
                )
                return response.text
            except Exception:
                return "Still rate limited. Please wait a minute and try again."
        
        # Invalid API Key
        elif "403" in error_message or "PERMISSION_DENIED" in error_message:
            return "API Key error. Please check your .env file."
        
        # No Internet
        elif "ConnectionError" in error_message:
            return "No internet connection. Please check your network."
        
        # Unknown Error
        else:
            return f"Unexpected error: {error_message[:100]}"

# Command Functions

def show_help() -> None:
    """Displays the list of available slash commands."""
    print(f"""
    {"=" * 45}
           {BOT_NAME} - Available Commands
    {"=" * 45}
      /help     Shows this help message
      /clear    Clear conversation memory
      /history  Show conversation history
      quit     Exit the chatbot
    {"=" * 45}
        """)
    
def show_history(chat_history: list) -> None:
        """
        Prints the full conversation history in a readable format.
        
        Args:
            chat_history (list): The conversation history to display
        """
        if not chat_history:
            print(f"\n{BOT_NAME}: No conversation history yet!\n")
            return
        
        print("\n" + "=" * 45)
        print("     Conversation History")
        print("=" * 45)
        
        for message in chat_history:
            role = message["role"]
            text = message["parts"][0]["text"]
            label = "You " if role == "user" else BOT_NAME
            print(f"\n  {label} : {text}")
            
        print("\n" + "=" * 45 + "\n")
        
def handle_command(command: str, chat_history: list) -> None:
    """
    Processes slash commands entered by the user.
    
    Args:
        command (str): The command string (e.g. '/help')
        chat_history (list): Passed to commands that need it
    """
    command = command.lower().strip()
    
    if command == "/help":
        show_help()
    elif command == "/clear":
        chat_history.clear()
        print(f"\n{BOT_NAME}: Memory cleared! Fresh start\n")
    elif command == "/history":
        show_history(chat_history)
    else:
        print(f"\n{BOT_NAME}: Unknown command '{command}'. Type /help for help.\n")
        
# Main Loop

def main() -> None:
    """
    Main function - runs the chatbot loop.
    Initialises the client, then handles user input continuously until the user types 'quit' or presses Ctrl+C.
    """
    # Initiaises Gemini Client
    client = initialise_client()
    
    # Welcome Message
    print("=" * 45)
    print(f"    Welcome to {BOT_NAME} - Your AI Assistant")
    print(f"  Created by {CREATOR_NAME} | Type /help for commands")
    print("=" * 45)
    
    # Conversation Memory
    chat_history = []
    
    while True:
        try: 
            user_input = input("\nYou: ").strip()
        except KeyboardInterrupt:
            print(f"\n\n{BOT_NAME}: Caught a Ctrl+C! Goodbye!")
            break
        
        # Empty Input
        if not user_input:
            print(f"{BOT_NAME}: Please type something!")
            continue
        
        # Quit
        if user_input.lower() == "quit":
            print(f"{BOT_NAME}: Goodbye! Keep Learning and stay awesome!")
            break
        
        # Slash Commands
        if user_input.startswith("/"):
            handle_command(user_input, chat_history)
            continue
        
        # Send to Gemini
        add_message(chat_history, "user", user_input)
        print(f"{BOT_NAME}: Thinking...")
        reply = get_ai_response(client, chat_history)
        print(f"\n{BOT_NAME}: {reply}")
        add_message(chat_history, "model", reply)
        
# Entry Point
if __name__ == "__main__":
    main()