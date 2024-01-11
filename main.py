import telebot
from typing import Final
import os
import datetime
import json
import requests


TOKEN: Final = '6045352877:AAESQ-r1Af5mH2GFXpNkIL4Gzo7jO8RMQQw'
BOT_USERNAME: Final = '@aclskjvouwqBot'
OUTPUT_FOLDER: Final = 'C:\\ComfyUI_windows_portable\\ComfyUI\\output'
INPUT_FOLDER: Final = '/mnt/c/ComfyUI_windows_portable/ComfyUI/input'
URL: Final = "http://127.0.0.1:8188/prompt"


# Create a new bot instance
bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
  bot.reply_to(message, "Похуй абсолютно")


def download_image(message) -> str:
  if message.photo is None:
    bot.reply_to(message, "Ты мне мозги не еби да")
    return
  # Download the photo to the output folder
  file_id = message.photo[-1].file_id
  file_info = bot.get_file(file_id)
  downloaded_file = bot.download_file(file_info.file_path)

  current_datetime = datetime.datetime.now()
  filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + '.jpg'
  username = message.from_user.username
  
  user_folder = os.path.join(INPUT_FOLDER, username)
  os.makedirs(user_folder, exist_ok=True)
  
  src = os.path.join(user_folder, filename)

  with open(src, 'wb') as new_file: 
    new_file.write(downloaded_file)
  print(f"Downloaded image to {src}")
  return filename
  
def send_prompt(prompt_workflow):
  print('sending prompt...')
  p = {"prompt": prompt_workflow}
  data = json.dumps(p).encode('utf-8')
  with requests.post(URL, data=data):
    print('prompt sent!')
  

@bot.message_handler(commands=['canny'])
def canny(message):
  bot.reply_to(message, 'send me pic')
  bot.register_next_step_handler(message, canny_something)


def canny_something(message):
  if message.photo is None:
    bot.reply_to(message, "Ты мне мозги не еби да")
    return
  bot.reply_to(message, "Thanks for the photo! I'll take that")
  fileName = download_image(message)

  print(fileName)
  with open("canny.json", "r") as file_json:
      print('opening json...')
      prompt = json.load(file_json)        
  username = message.from_user.username
  prompt["2"]["inputs"]["image"] = f"{username}/{fileName}"
  # send_prompt(prompt)
  print('sending prompt...')


# async def senend_image(message, filename):
  

def main():
  print("ну че ебаный рот погнали нахуй")
  bot.polling()


if __name__ == "__main__":
  main()