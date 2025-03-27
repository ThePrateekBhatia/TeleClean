from pyrogram import Client
import os

def get_user_client():
    session_string = os.getenv("SESSION_STRING")
    if not session_string:
        return None  # No session string provided

    return Client(
        name="user_client",
        api_id=int(os.getenv("API_ID")),
        api_hash=os.getenv("API_HASH"),
        session_string=session_string
    )
