from telepot import Bot
from configparser import ConfigParser

config = ConfigParser()
config.read("config-original.ini")

TOKEN = config.get("bot", "token")

bot = Bot(TOKEN)

ID = bot.getUpdates()[-1]["message"]["chat"]["id"]


def send_msg(message: str, id: str = ""):
    if not id:
        id = ID
    bot.sendMessage(id, message)


def send_image(image, id: str = ""):
    if not id:
        id = ID
    bot.sendPhoto(id, image)