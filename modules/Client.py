from os import getenv
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

app = Client(
    "UwU",
    api_id=getenv("API_ID"), 
    api_hash=getenv("API_HASH"),
    bot_token=getenv("BOT_TOKEN")
)

ID_CHANNEL = getenv('ID_CHANNEL')