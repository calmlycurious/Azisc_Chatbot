# Azisc — AI Chatbot

A conversational AI chatbot built with Python and Google's Gemini API.

## Features
- Multi-turn conversation with memory
- Custom AI persona via system prompt
- Slash commands (/help, /clear, /history)
- Graceful error handling
- Clean, modular code structure

## Tech Stack
- Python 3.13
- Google Gemini API (gemini-2.5-flash-lite)
- python-dotenv

## Setup & Installation

1. Clone the repository<br>
   git clone https://github.com/calmlycurious/Azisc_Chatbot.git

2. Create and activate virtual environment<br>
   python3 -m venv venv<br>
   source venv/bin/activate

3. Install dependencies<br>
   pip3 install google-genai<br>
   python-dotenv

4. Create a .env file and add your Gemini API key<br>
   GEMINI_API_KEY=your_api_key_here

5. Run the chatbot<br>
   python3 chatbot.py

## Commands
| Command | Description |
|---------|-------------|
| /help | Show available commands |
| /clear | Clear conversation memory |
| /history | Show conversation history |
| quit | Exit the chatbot |

## Author
Ashish Gurung | BCA 2nd Year Student | Siliguri | Passionate about AI and Machine Learning