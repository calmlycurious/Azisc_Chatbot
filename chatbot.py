from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_ai_response(user_message):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_message
    )
    return response.text

def main():
    print("=" * 45)
    print("     Welcome to Azisc — Your AI Assistant")
    print("     Type 'quit' to exit")
    print("=" * 45)

    while True:
        user_input = input("\nYou: ").strip()
        
        if not user_input:
            print("Azisc: Please type something!")
            continue

        if user_input.lower() == "quit":
            print("Azisc: Goodbye! Have a great day.")
            break

        print("Azisc: Thinking...")
        reply = get_ai_response(user_input)
        print(f"Azisc: {reply}")

if __name__ == "__main__":
    main()