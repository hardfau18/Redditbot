# echo.py
# Example:
# randomuser - "!echo example string"
# echo_bot - "example string"

import simplematrixbotlib as botlib
import os

server = os.environ.get("MATRIX_SERVER")
user_name = os.environ.get("REDITBOTUNAME")
password = os.environ.get("REDITPASSWORD")

creds = botlib.Creds(server, user_name, password)
bot = botlib.Bot(creds)
PREFIX = '!'

def ech(msg:str)->str:
    return msg.upper()

@bot.listener.on_message_event
async def echo(room, message):
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix() and match.command("echo"):
        msg = ech(" ".join(arg for arg in match.args()))
        await bot.api.send_text_message(room.room_id, msg)

bot.run()
