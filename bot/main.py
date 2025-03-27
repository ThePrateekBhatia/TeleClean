import asyncio
import os
from dotenv import load_dotenv
from bot.session import connect_user
from bot.bot_connect import connect_bot
from bot.helper.delete import delete_user_messages, delete_all_messages

load_dotenv()

async def main():
    # Load environment variables
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    session_string = os.getenv("SESSION_STRING")
    chat_id = int(os.getenv("CHAT_ID"))
    user_msgs_duration = int(os.getenv("USER_MSGS_DURATION"))
    overall_msgs_duration = int(os.getenv("OVERALL_MSGS_DURATION"))
    owner_id = int(os.getenv("OWNER_ID"))

    # Determine connection mode
    client = None
    if session_string:
        print("🔗 Connecting via user session...")
        client = await connect_user(api_id, api_hash, session_string)
        asyncio.create_task(delete_all_messages(client, chat_id, overall_msgs_duration, owner_id))
    elif bot_token:
        print("🤖 Connecting via bot token...")
        client = await connect_bot(api_id, api_hash, bot_token)
        asyncio.create_task(delete_user_messages(client, chat_id, user_msgs_duration, owner_id))
    else:
        print("❌ No valid connection provided (BOT_TOKEN or SESSION_STRING required).")
        return

    print("🚀 Bot is running and monitoring messages.")
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())
