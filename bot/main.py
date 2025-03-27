import asyncio
import os
from bot.session import get_user_client
from bot.bot_connect import get_bot_client
from bot.helper.handler import process_deletion

async def main():
    print("🔍 Initializing TeleClean Bot...")

    # Load environment variables
    session_string = os.getenv("SESSION_STRING")
    bot_token = os.getenv("BOT_TOKEN")

    # Determine which client to use
    user_client = get_user_client() if session_string else None
    bot_client = get_bot_client() if bot_token else None

    if not user_client and not bot_client:
        print("❌ No valid session or bot token provided. Exiting...")
        return

    # Start appropriate clients
    if user_client:
        print("✅ User session detected. Connecting...")
        await user_client.start()
    if bot_client:
        print("✅ Bot token detected. Connecting...")
        await bot_client.start()

    # Perform message deletion
    try:
        await process_deletion(user_client, bot_client)
    finally:
        # Ensure proper disconnection
        if user_client:
            await user_client.stop()
        if bot_client:
            await bot_client.stop()

    print("✅ Cleanup completed.")

if __name__ == "__main__":
    asyncio.run(main())
