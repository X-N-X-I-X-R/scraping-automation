from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Create a new instance of a ChatBot
chatbot = ChatBot('PDF_Translated_ChatBot')

# Create a new trainer for the chatbot
trainer = ListTrainer(chatbot)

# Load the lines from the file
with open('translated.txt', 'r') as f:
    lines = f.read().splitlines()

# Train the chatbot based on the lines
trainer.train(lines)

def get_response(user_input):
  response = str(chatbot.get_response(user_input))
  return response[::-1]

