import asyncio
import os
from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.errors import FloodWait

from bot.helper.data_handler import save_messages

async def collect_messages(client, chat_id, duration, delete_type, owner_client, owner_id):
    """
    Collects messages for deletion within the specified time duration.

    Args:
    - client: Telegram client (bot or user session).
    - chat_id (int): ID of the chat to clean.
    - duration (int): Time window (in seconds) to fetch messages.
    - delete_type (str): Type of deletion ('user' or 'overall').
    - owner_client: User session client to send logs.
    - owner_id (int): Telegram ID of the bot owner.
    """
    try:
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=duration)

        # Collecting messages
        messages_to_delete = []
        async for message in client.get_chat_history(chat_id, limit=5000):
            if message.date < cutoff_time:
                break

            # Delete only user messages if using BOT_TOKEN
            if delete_type == "user" and not message.from_user.is_bot:
                messages_to_delete.append(message)
            elif delete_type == "overall":
                messages_to_delete.append(message)

        print(f"🗑️ Collected {len(messages_to_delete)} messages for {delete_type} deletion.")

        # Save collected messages (if user session is available)
        if messages_to_delete and owner_client and owner_id:
            await save_messages(messages_to_delete, owner_client, owner_id)

        return messages_to_delete

    except FloodWait as e:
        print(f"⏳ Rate limited. Waiting for {e.value} seconds...")
        await asyncio.sleep(e.value)
    except Exception as error:
        print(f"❌ Error in message collection: {error}")

async def message_handler(bot_client=None, user_client=None):
    """
    Main handler to collect and process messages for deletion.

    Args:
    - bot_client: Pyrogram bot client (optional).
    - user_client: Pyrogram user client (optional).
    """
    chat_id = int(os.getenv("CHAT_ID"))
    user_duration = int(os.getenv("USER_MSGS_DURATION", 0))
    overall_duration = int(os.getenv("OVERALL_MSGS_DURATION", 0))
    owner_id = int(os.getenv("OWNER_ID", 0))

    print(f"📊 Monitoring Chat ID: {chat_id}")
    print(f"🔍 User Msgs Delete After: {user_duration}s, Overall Delete After: {overall_duration}s")

    # User message cleanup (BOT_TOKEN)
    if bot_client and user_duration > 0:
        user_messages = await collect_messages(bot_client, chat_id, user_duration, "user", user_client, owner_id)
        return user_messages

    # Overall cleanup (SESSION_STRING)
    if user_client and overall_duration > 0:
        overall_messages = await collect_messages(user_client, chat_id, overall_duration, "overall", user_client, owner_id)
        return overall_messages
