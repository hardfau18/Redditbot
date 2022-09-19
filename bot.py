# echo.py
# Example:
# randomuser - "!echo example string"
# echo_bot - "example string"

import simplematrixbotlib as botlib
import os
import random

class ReditBot(botlib.Bot):
    def __init__(self, server, user_name, password, store_path="./crypto_store/", encryption_enabled=True, prefix="!"):
        self.config = botlib.Config()
        self.shutup_count = 0
        self.prefix = prefix
        self.config.encryption_enabled = encryption_enabled
        self.config.store_path = store_path
        self.creds = botlib.Creds(server, user_name, password)
        super().__init__(self.creds, self.config)
        self.listener.on_message_event(self.on_message)

    async def on_message(self, room, message):
        global count
        match = botlib.MessageMatch(room, message, self, self.prefix)
        if match.is_not_from_this_bot():
            if match.prefix():
                if self.shutup_count<= 0:
                    msg = self.echo(message.body[1:])
                    await self.api.send_text_message(room.room_id, msg)
                else:
                    count -= 1
                    await self.api.send_text_message(room.room_id, "🙊")
            elif match.contains("shutup bot"):
                self.shutup_count = random.randint(1,11)
                await self.api.send_text_message(room.room_id, "😥")

    def echo(self, msg:str)->str:
        return msg.upper()



if __name__ == "__main__":
    server = os.environ.get("MATRIX_SERVER")
    user_name = os.environ.get("REDITBOTUNAME")
    password = os.environ.get("REDITPASSWORD")
    bot = ReditBot(server, user_name, password)
    bot.run()
