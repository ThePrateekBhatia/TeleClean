import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure Python recognizes 'bot/' directory
sys.path.append(os.path.dirname(__file__))

from session import connect_user
from bot_connect import connect_bot
from helper.delete import delete_user_messages, delete_all_messages

load_dotenv()

async def main():
    user_client = await connect_user()
    bot_client = await connect_bot()
    print("✅ Both User and Bot Clients Connected Successfully!")

    user_msgs_duration = int(os.getenv("USER_MSGS_DURATION", 0))
    overall_msgs_duration = int(os.getenv("OVERALL_MSGS_DURATION", 0))

    if user_msgs_duration > 0:
        asyncio.create_task(delete_user_messages(user_client, user_msgs_duration))
    if overall_msgs_duration > 0:
        asyncio.create_task(delete_all_messages(bot_client, overall_msgs_duration))

    await asyncio.gather(user_client.run(), bot_client.run())

if __name__ == "__main__":
    asyncio.run(main())
