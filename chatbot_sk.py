bot_name = "Azisc"
print(f"Hi! I am {bot_name}. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print(f"{bot_name}: Goodbye! Have a great day.")
        break
    elif user_input.lower() == "hello":
        print(f"{bot_name}: Hello there! How can I help you?")
    else:
        print(f"{bot_name}: You said '{user_input}'. I am still learning!")        