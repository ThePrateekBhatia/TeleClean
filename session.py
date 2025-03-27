from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Enter your API ID: "))
api_hash = input("Enter your API Hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("Your session string:")
    print(session_string)

    # Send the session string to Saved Messages
    client.send_message("me", f"#SessionString #Telethon #TeleClean\n`{session_string}`")
    print("Session string sent to your Saved Messages.")
