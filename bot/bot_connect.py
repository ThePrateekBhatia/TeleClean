from pyrogram import Client
import os

def get_bot_client():
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        return None  # No bot token provided

    return Client(
        name="bot_client",
        api_id=int(os.getenv("API_ID")),
        api_hash=os.getenv("API_HASH"),
        bot_token=bot_token
    )
