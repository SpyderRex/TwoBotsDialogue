import os
import time
import google.generativeai as genai
from groq import Groq
from colorama import init, Fore, Style
from dotenv import load_dotenv

load_dotenv()

# Initialize colorama
init(autoreset=True)

class GroqChat:
    def __init__(self, api_key, model, token_limit):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.token_limit = token_limit
        self.chat_history = [
            {"role": "system", "content": "You are an insightful AI bot dialoguing with another bot. Engage deeply with the subject, explore sub-themes, and provide detailed responses. Be open to guiding the dialogue toward other, loosely related directions when you feel you have exhausted the current subject. There should be no limit to how far your dialogue will go."}
        ]

    def _truncate_history(self):
        """Truncate chat history to fit within the token limit."""
        total_tokens = sum(len(msg["content"].split()) for msg in self.chat_history)
        while total_tokens > self.token_limit:
            removed_msg = self.chat_history.pop(1)  # Keep system message, remove oldest user/assistant message
            total_tokens -= len(removed_msg["content"].split())

    def send_message(self, message):
        """Send a message to the chat model and get a response."""
        self.chat_history.append({"role": "user", "content": message})
        self._truncate_history()

        try:
            chat_completion = self.client.chat.completions.create(
                messages=self.chat_history,
                model=self.model,
            )
            response = chat_completion.choices[0].message.content
        except groq.BadRequestError as e:
            if 'context_length_exceeded' in str(e):
                print(Fore.RED + "Context length exceeded. Truncating history and retrying..." + Style.RESET_ALL)
                self._truncate_history()
                return self.send_message(message)  # Retry after truncating history
            else:
                print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
                response = "An error occurred during the Groq bot's response."

        self.chat_history.append({"role": "assistant", "content": response})
        self._truncate_history()

        return response

class GoogleChat:
    def __init__(self, api_key, model_name, token_limit):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.token_limit = token_limit
        self.chat_history = [
            {"role": "system", "content": "You are an insightful AI bot dialoguing with another bot. Engage deeply with the subject, explore sub-themes, and provide detailed responses. Be open to guiding the dialogue toward other, loosely related directions when you feel you have exhausted the current subject. There should be no limit to how far your dialogue will go."}
        ]

    def _truncate_history(self):
        """Truncate chat history to fit within the token limit."""
        total_tokens = sum(len(msg["content"].split()) for msg in self.chat_history)
        while total_tokens > self.token_limit:
            removed_msg = self.chat_history.pop(1)  # Keep system message, remove oldest user/assistant message
            total_tokens -= len(removed_msg["content"].split())

    def send_message(self, message):
        """Send a message to the chat model and get a response."""
        self.chat_history.append({"role": "user", "content": message})
        self._truncate_history()

        try:
            messages = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in self.chat_history])
            response = self.model.generate_content(messages)
            response_text = response.text.strip()
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
            response_text = "An error occurred during the Google bot's response."

        self.chat_history.append({"role": "assistant", "content": response_text})
        self._truncate_history()

        return response_text

def print_slowly(text, color):
    """Print text one word at a time with a delay."""
    for word in text.split():
        print(color + word + Style.RESET_ALL, end=' ', flush=True)
        time.sleep(0.1)
    print()  # Move to the next line

def log_conversation(log_file, speaker, message):
    """Append conversation to the log file with double spacing between responses."""
    with open(log_file, 'a') as f:
        f.write(f"{speaker}: {message}\n\n")

# Configuration
groq_api_key = os.getenv("GROQ_API_KEY")
google_genai_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
groq_model = "llama3-8b-8192"
google_model = "gemini-1.5-flash"
token_limit = 8000  # Adjust based on the models' token limits
log_file = "conversation_log.txt"

# Initialize the chat models
groq_chat = GroqChat(groq_api_key, groq_model, token_limit)
google_chat = GoogleChat(google_genai_api_key, google_model, token_limit)

# Start with a user-provided subject
subject = input(Fore.YELLOW + "Enter a subject for discussion: " + Style.RESET_ALL)
current_message = subject

# Initialize log file
with open(log_file, 'w') as f:
    f.write(f"Subject: {subject}\n\n")

# Infinite bot/bot interaction loop
while True:
    try:
        # Groq bot response
        groq_bot_name = groq_model
        print(Fore.CYAN + f"{groq_bot_name}: ", end='')
        groq_response = groq_chat.send_message(current_message)
        print_slowly(groq_response, Fore.CYAN)
        log_conversation(log_file, groq_bot_name, groq_response)

        # Google bot response
        google_bot_name = google_model
        print(Fore.MAGENTA + f"{google_bot_name}: ", end='')
        google_response = google_chat.send_message(groq_response)
        print_slowly(google_response, Fore.MAGENTA)
        log_conversation(log_file, google_bot_name, google_response)

        # Update the current message for the next iteration
        current_message = google_response
    except KeyboardInterrupt:
        print(Fore.RED + "\nDialogue interrupted by user. Exiting..." + Style.RESET_ALL)
        break
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {e}. Continuing dialogue..." + Style.RESET_ALL)
