import asyncio
from pyrogram.errors import FloodWait

async def delete_messages(client, chat_id, messages):
    """
    Deletes a batch of messages from a given chat.

    Args:
    - client: Pyrogram client (bot or user session).
    - chat_id (int): Target chat ID for message deletion.
    - messages (list): List of message IDs to delete.
    """
    if not messages:
        print("✅ No messages to delete.")
        return

    try:
        # Batch deletion (max 100 messages per request)
        for i in range(0, len(messages), 100):
            batch = [msg.id for msg in messages[i:i + 100]]
            await client.delete_messages(chat_id, batch)
            print(f"🗑️ Deleted {len(batch)} messages.")
            await asyncio.sleep(2)  # To avoid hitting rate limits

    except FloodWait as e:
        print(f"⏳ Rate limited. Waiting for {e.value} seconds...")
        await asyncio.sleep(e.value)
        await delete_messages(client, chat_id, messages)  # Retry after waiting

    except Exception as error:
        print(f"❌ Error while deleting messages: {error}")
