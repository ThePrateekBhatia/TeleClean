import asyncio
import os
from dotenv import load_dotenv
from bot.session import connect_user
from bot.bot_connect import connect_bot
from bot.helper.delete import delete_user_messages, delete_all_messages

# Load environment variables from .env file
load_dotenv()

async def main():
    # Connect to User and Bot Clients
    user_client = await connect_user()
    bot_client = await connect_bot()

    print("✅ Both User and Bot Clients Connected Successfully!")

    # Start message deletion handlers
    user_msgs_duration = int(os.getenv("USER_MSGS_DURATION", 0))
    overall_msgs_duration = int(os.getenv("OVERALL_MSGS_DURATION", 0))

    if user_msgs_duration > 0:
        asyncio.create_task(delete_user_messages(user_client, user_msgs_duration))

    if overall_msgs_duration > 0:
        asyncio.create_task(delete_all_messages(bot_client, overall_msgs_duration))

    # Keep the event loop running
    await asyncio.gather(user_client.run(), bot_client.run())

if __name__ == "__main__":
    asyncio.run(main())
