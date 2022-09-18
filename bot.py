# echo.py
# Example:
# randomuser - "!echo example string"
# echo_bot - "example string"

import simplematrixbotlib as botlib
import os
import random

server = os.environ.get("MATRIX_SERVER")
user_name = os.environ.get("REDITBOTUNAME")
password = os.environ.get("REDITPASSWORD")
count = 0

config = botlib.Config()
config.encryption_enabled = True
config.store_path = './crypto_store/'

creds = botlib.Creds(server, user_name, password)
bot = botlib.Bot(creds, config)
PREFIX = '!'

def ech(msg:str)->str:
    return msg.upper()

@bot.listener.on_message_event
async def echo(room, message):
    global count
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot():
        if match.prefix():
            if count <= 0:
                msg = ech(message.body[1:])
                await bot.api.send_text_message(room.room_id, msg)
            else:
                count -= 1
                await bot.api.send_text_message(room.room_id, "🙊")
        elif match.contains("shutup bot"):
            count = random.randint(1,11)
            await bot.api.send_text_message(room.room_id, "😥")
bot.run()
