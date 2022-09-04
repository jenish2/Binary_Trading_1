# Author : Jenish Dholariya
import json
import os

from Bot.bot import Bot

with open(os.path.join(os.path.dirname(__file__), "User_Input/settings.json")) as file:
    configuration = json.load(file)
    file.close()

with open(os.path.join(os.path.dirname(__file__), "User_Input/credentials.json")) as file:
    credentials = json.load(file)
    file.close()

bot = Bot(credentials=credentials, configuration=configuration)
bot.start()
