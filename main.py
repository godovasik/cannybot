import time
import telebot
from typing import Final
import os
import datetime
import json
import requests
from PIL import Image
import random

"""
  TODO:
    add queue
    mulitprocessing
    buttons instead of commands



"""



TOKEN: Final = '6200012580:AAGkanLFVbczjH59llA-3huAVE1rnT49Gho'
BOT_USERNAME: Final = '@aclskjvouwqBot'
OUTPUT_FOLDER: Final = 'C:\\ComfyUI_windows_portable\\ComfyUI\\output'
INPUT_FOLDER: Final = 'C:\\ComfyUI_windows_portable\\ComfyUI\\input'
WORK_FOLDER: Final = 'C:\\bots\\cannybot'
URL: Final = "http://127.0.0.1:8188/prompt"
MAX_INT: Final = 2**63 - 1

WORKFLOWS  = { # json_name: needs_resize
  "canny": False,
  # "animerge": True,
  # "inpaint" : False,
  "anim_tile": True,
  "btw": False,
  "dream_portrait": False,
  "cartoon_portrait": False,
}


# Create a new bot instance
bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "hi! Выбери команду из менюшки ")
  if getQ() is None:
    bot.send_message(message.chat.id, "comfy is not running, starting...")
    restart_comfy()

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, "наебал")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
  bot.reply_to(message, "сначала выбери команду, потом присылай картинку")

@bot.message_handler(commands=list(WORKFLOWS.keys()))
def model_handler(message):
  bot.reply_to(message, 'send me pic')
  json_name = message.text[1:]
  bot.register_next_step_handler(message, img2img, json_name=json_name)


def download_image(message, json_name): # filename: username_workflow
  # Download the photo to the output folder
  file_id = message.photo[-1].file_id # get the file_id of the last (biggest) photo sent
  file_info = bot.get_file(file_id)
  downloaded_file = bot.download_file(file_info.file_path)

  username = message.from_user.username

  current_datetime = datetime.datetime.now()
  filename = f"{username}_{json_name}_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
  
  user_folder = os.path.join(INPUT_FOLDER, username)
  os.makedirs(user_folder, exist_ok=True)
  
  src = os.path.join(user_folder, filename)

  with open(src, 'wb') as new_file: 
    new_file.write(downloaded_file)
  print(f"Downloaded image to {src}")
  return filename
  
def send_prompt(prompt_workflow):
  print('sending workflow...')
  p = {"prompt": prompt_workflow}
  data = json.dumps(p).encode('utf-8')
  requests.post(URL, data=data)

  




def img2img(message, json_name):
  if message.photo is None:
    bot.reply_to(message, "it's not a pic bro cmon")
    return
  fileName = download_image(message, json_name=json_name) # username_workflowDate

  username = message.from_user.username

  if WORKFLOWS[json_name]: #if needs resize
    resize_image(os.path.join(INPUT_FOLDER, username, fileName))

  print(f"Saved: {fileName}")
  with open(os.path.join(WORK_FOLDER, "workflows", json_name + ".json" ), "r") as file_json:
      workflow = json.load(file_json)
  
  prefix = fileName.removesuffix(".jpg")
  
  loadID = find_nodeID_by_type(workflow, "LoadImage")
  prefixID = find_nodeID_by_type(workflow, "SaveImage")
  ksamplerID = find_nodeID_by_type(workflow, "KSampler")

  workflow[loadID]["inputs"]["image"] = f"{username}\\{fileName}"
  workflow[prefixID]["inputs"]["filename_prefix"] = prefix
  try: 
    workflow[ksamplerID]["inputs"]["seed"] = random.randint(1, MAX_INT)
  except:
    pass
  
  send_prompt(workflow)
  bot.reply_to(message, f"got it, yor position in queue is {getQ()}")  
  output_image = os.path.join(OUTPUT_FOLDER, f"{prefix}_00001_.png")
  send_result(message, output_image)

def send_result(message, output_image):
  x: int = 0
  while True:
    if os.path.exists(output_image):
      try:
        bot.send_photo(message.chat.id, open(output_image, 'rb'))
      except Exception as e:
        bot.send_message(message.chat.id, "error sending image, unlucky")
        print(e)
        restart_comfy()
      print("send")
      return
    time.sleep(1)
    x+=1
    if x > 300:
      bot.reply_to(message, "runtime error, unlucky")
      restart_comfy()


def prompt_handler(message, workflow, json_name, prefix):
  bot.send_message(message.chat.id, "processing...")
  workflow[WORKFLOWS[json_name][1]]["inputs"]["text"] = message.text
  send_prompt(workflow)
  while True:
    if os.path.exists(f"{OUTPUT_FOLDER}\\{prefix}_00001_.png"):
      bot.send_photo(message.chat.id, open(f"{OUTPUT_FOLDER}\\{prefix}_00001_.png", 'rb'))
      return
    time.sleep(1)

def resize_image(image_path):
  image = Image.open(image_path)
  min_size = 512
  width, height = image.size

  if width < height:
    new_width = min_size
    new_height = int(height * (min_size / width) // 8 * 8)
  else:
    new_height = min_size
    new_width = int(width * (min_size / height) // 8 * 8)

  resized_image = image.resize((new_width, new_height))
  resized_image.save(image_path)

def find_nodeID_by_type(workflow, type):
  for k in workflow:
    if workflow[k]["class_type"] == type:
      return str(k)

def restart_comfy():
  os.system("taskkill /f /im cmd.exe /T")
  time.sleep(2)
  os.system("start C:\\ComfyUI_windows_portable\\run_nvidia_gpu.bat")
  print("comfy restarting...")
  while getQ() is None:
    time.sleep(3)                                      
  print("ready to serve you sir")

def getQ():
  try:
    lol = requests.get(URL)
  except:
    return None
  return lol.json()['exec_info']['queue_remaining']

def main():
  if getQ() is None:
    print("comfy is not running, starting...")
    restart_comfy()
    
  print("ну че ебаный рот погнали нахуй")
  bot.polling()


if __name__ == "__main__":
  main()