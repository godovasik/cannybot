import telebot
from typing import Final
import os
import datetime
import json

TOKEN: Final = '6045352877:AAESQ-r1Af5mH2GFXpNkIL4Gzo7jO8RMQQw'
BOT_USERNAME: Final = '@aclskjvouwqBot'
OUTPUT_FOLDER: Final = 'C:\\ComfyUI_windows_portable\\ComfyUI\\output'
INPUT_FOLDER: Final = '/mnt/c/ComfyUI_windows_portable/ComfyUI/input'


# Create a new bot instance
bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Howdy, how are you doing?")

# Handle text messages
@bot.message_handler(content_types=['text'])
def handle_text_message(message):
  bot. reply_to(message, message.text)

# Handle photo messages
@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
  # Reply to the user with a confirmation message
  bot.reply_to(message, "Thanks for the photo! I'll take that")
  # Download the photo to the output folder
  file_id = message.photo[-1].file_id
  file_info = bot.get_file(file_id)
  downloaded_file = bot.download_file(file_info.file_path)
  
  current_datetime = datetime.datetime.now()
  filename = current_datetime.strftime("%Y.%m.%d_%H:%M:%S") + '.jpg'
  src = os.path.join(INPUT_FOLDER, filename)
  
  with open(src, 'wb') as new_file: 
    new_file.write(downloaded_file)
  print(f"Downloaded image to {src}")
  
  # Process the image





def main():
  print("ну че ебаный рот погнали нахуй")
  bot.polling()


if __name__ == "__main__":
  main()