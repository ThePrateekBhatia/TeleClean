import asyncio

async def delete_messages(clients, chat_id, message_ids):
    """
    Deletes messages from a chat using provided clients (user session/bot client).

    Args:
    - clients (list): List of active clients (user or bot).
    - chat_id (int): Target chat ID where messages will be deleted.
    - message_ids (list): List of message IDs to delete.
    """
    batch_size = 100  # Maximum batch size for bulk deletion
    total_deleted = 0

    # Delete messages in chunks to avoid exceeding API limits
    for i in range(0, len(message_ids), batch_size):
        batch = message_ids[i:i + batch_size]

        for client in clients:
            try:
                await client.delete_messages(chat_id, batch, revoke=True)
                total_deleted += len(batch)
                print(f"✅ Deleted {len(batch)} messages via {client.__class__.__name__}")
            except Exception as e:
                print(f"❌ Error while deleting messages: {e}")
            
            # Prevent floodwait issues
            await asyncio.sleep(1)

    print(f"🗑️ Total Messages Deleted: {total_deleted}")
