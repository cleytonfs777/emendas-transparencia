import os

import aiohttp
from telegram import Bot, InputFile
from telegram.error import BadRequest

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/"

async def send_telegram_message(chat_id, message_text):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{API_URL}sendMessage",
                data={"chat_id": chat_id, "text": message_text},
            ) as response:
                await response.json()
        except Exception as e:
            print(f"Unexpected error sending message: {e}")

async def send_telegram_image(chat_id, image_path):
    async with aiohttp.ClientSession() as session:
        try:
            with open(image_path, "rb") as image_file:
                form_data = aiohttp.FormData()
                form_data.add_field("chat_id", str(chat_id))
                form_data.add_field("photo", image_file, filename="image.jpg")
                async with session.post(f"{API_URL}sendPhoto", data=form_data) as response:
                    await response.json()
        except Exception as e:
            print(f"Unexpected error sending image: {e}")
