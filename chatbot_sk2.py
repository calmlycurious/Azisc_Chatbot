def get_user_input():
    return input("You: ").strip()

def handle_command(command, chat_history):
    if command == "/quit":
        print("Bot: Goodbye! See you soon.")
        return False
    elif command == "/help":
        print("Bot: Available commands -> /quit, /help, /clear")
        return True
    elif command == "/clear":
        chat_history.clear()
        print("Bot: Conversation cleared!")
        return True
    return True

def main():
    print("=" * 40)
    print("Welcome to Azisc Chatbot")
    print("Type /help for commands")
    print("=" * 40)
    
    chat_history = []
    bot_name = "Azisc"
    
    while True:
        user_input = get_user_input()
        
        if not user_input:
            print(f"{bot_name}: Please type something!")
            continue
        
        if user_input.startswith("/"):
            should_continue = handle_command(user_input.lower(), chat_history)
            if not should_continue:
                break
            continue
        
        chat_history.append({"role": "user", "content": user_input})
        
        bot_reply = f"I heard you say: '{user_input}'. AI coming soon!"
        print(f"{bot_name}: {bot_reply}")
        
        chat_history.append({"role": "model", "content": bot_reply})
        
if __name__ == "__main__":
    main()