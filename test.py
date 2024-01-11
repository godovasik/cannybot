import json
import requests
import asyncio

from telebot.async_telebot import AsyncTeleBot

TOKEN = '6045352877:AAESQ-r1Af5mH2GFXpNkIL4Gzo7jO8RMQQw'

bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
  await bot.reply_to(message, "hi")

@bot.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
  await bot.reply_to(message, "Похуй абсолютно")

def main():
  print("го")
  asyncio.run(bot.polling())

if __name__ == '__main__':
  main()