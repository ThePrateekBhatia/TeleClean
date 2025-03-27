import asyncio
import datetime
from pyrogram.errors import FloodWait
from .data_handler import handle_deleted_data

async def delete_user_messages(client, chat_id, duration, owner_id):
    """
    Deletes user messages after a given duration.

    Args:
    - client: Pyrogram client (bot mode).
    - chat_id (int): Target chat ID.
    - duration (int): Time in seconds after which messages are deleted.
    - owner_id (int): Owner ID for message logs.
    """
    print(f"🔍 Monitoring user messages in {chat_id}...")

    while True:
        try:
            # Time window to delete messages
            cutoff_time = datetime.datetime.now() - datetime.timedelta(seconds=duration)

            # Collect messages for deletion and logging
            messages_to_delete = []
            async for msg in client.get_chat_history(chat_id, limit=500):
                if msg.date < cutoff_time and msg.from_user:
                    messages_to_delete.append(msg)

            if messages_to_delete:
                print(f"🗑️ Deleting {len(messages_to_delete)} user messages.")
                
                # Log deleted data before actual deletion
                await handle_deleted_data(client, messages_to_delete, owner_id)
                
                for msg in messages_to_delete:
                    try:
                        await client.delete_messages(chat_id, msg.message_id)
                        await asyncio.sleep(0.5)  # Avoid hitting rate limits
                    except FloodWait as e:
                        print(f"⏳ Rate limit hit. Sleeping for {e.x} seconds.")
                        await asyncio.sleep(e.x)
            else:
                print("✅ No user messages to delete.")

            # Wait and repeat
            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ Error during user message deletion: {e}")
            await asyncio.sleep(30)

async def delete_all_messages(client, chat_id, duration, owner_id):
    """
    Deletes all messages after a given duration (for user session mode).

    Args:
    - client: Pyrogram client (user mode).
    - chat_id (int): Target chat ID.
    - duration (int): Time in seconds after which messages are deleted.
    - owner_id (int): Owner ID for message logs.
    """
    print(f"🔍 Monitoring all messages in {chat_id}...")

    while True:
        try:
            cutoff_time = datetime.datetime.now() - datetime.timedelta(seconds=duration)

            # Collect all messages (visible chat history required)
            messages_to_delete = []
            async for msg in client.get_chat_history(chat_id, limit=500):
                if msg.date < cutoff_time:
                    messages_to_delete.append(msg)

            if messages_to_delete:
                print(f"🗑️ Deleting {len(messages_to_delete)} total messages.")
                
                # Log deleted data before actual deletion
                await handle_deleted_data(client, messages_to_delete, owner_id)
                
                for msg in messages_to_delete:
                    try:
                        await client.delete_messages(chat_id, msg.message_id)
                        await asyncio.sleep(0.5)
                    except FloodWait as e:
                        print(f"⏳ Rate limit hit. Sleeping for {e.x} seconds.")
                        await asyncio.sleep(e.x)
            else:
                print("✅ No messages to delete.")

            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ Error during message deletion: {e}")
            await asyncio.sleep(30)
