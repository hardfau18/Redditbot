# echo.py
# Example:
# randomuser - "!echo example string"
# echo_bot - "example string"

from __future__ import unicode_literals
import simplematrixbotlib as botlib
import os
import random
import youtube_dl as yd
import re
import asyncio
    

class ReditBot(botlib.Bot):
    def __init__(self, server, user_name, password, store_path="/crypto_store/", encryption_enabled=True, prefix="!"):
        self.config = botlib.Config()
        self.shutup_count = 0
        self.prefix = prefix
        self.config.encryption_enabled = encryption_enabled
        if not os.path.isdir(os.environ["HOME"]+"/.cache"):
            os.mkdir(os.environ["HOME"]+"/.cache")
        if not os.path.isdir(os.environ["HOME"]+"/.cache/ReditBot"):
            os.mkdir(os.environ["HOME"]+"/.cache/ReditBot")
        if not os.path.isdir(os.environ["HOME"]+"/.cache/ReditBot/Download"):
            os.mkdir(os.environ["HOME"]+"/.cache/ReditBot/Download")
        self.config.store_path = os.environ["HOME"]+"/.cache/ReditBot"+store_path
        self.creds = botlib.Creds(server, user_name, password)
        super().__init__(self.creds, self.config)
        self.listener.on_message_event(self.on_message)

    async def on_message(self, room, message):
        match = botlib.MessageMatch(room, message, self, self.prefix)
        if match.is_not_from_this_bot():
            if match.prefix():
                if self.shutup_count<= 0:
                    msg = self.echo(message.body[1:])
                    await self.api.send_text_message(room.room_id, msg)
                else:
                    self.shutup_count -= 1
                    await self.api.send_text_message(room.room_id, "🙊")

            elif match.contains("shutup bot"):
                self.shutup_count = random.randint(1,11)
                await self.api.send_text_message(room.room_id, "😥")

            elif match.contains("https://"):
                #print(message.body)
                res = self.is_redit_link(message.body)
                await self.api.send_text_message(room.room_id, res)

    def echo(self, msg:str)->str:
        return msg.upper()

    def is_redit_link(self, link:str)->str:
        check_link = re.compile(r"https://www.reddit.com/r/\S+\??")
        res = check_link.search(link)
        if res:
            url = res.group(0)
            ydl_opts = {'outtmpl': os.environ["HOME"]+"/.cache/ReditBot/Download/%(title)s.%(ext)s"}
            with yd.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                except Exception as e:
                    return "ERROR: "+e.__str__()[17:]
            return "Title"
        else:
            return "What the heck is this"

if __name__ == "__main__":
    server = os.environ.get("MATRIX_SERVER")
    user_name = os.environ.get("REDITBOTUNAME")
    password = os.environ.get("REDITPASSWORD")
    bot = ReditBot(server, user_name, password)
    while(True):
        try:
            bot.run()
        except asyncio.exceptions.TimeoutError:
            continue
        except Exception as e:
            print(e)
            break
