import os
import time
from bot.helper.delete import delete_messages
from bot.helper.data_handler import store_message_data

async def process_deletion(user_client, bot_client):
    chat_id = int(os.getenv("CHAT_ID"))
    user_msgs_duration = int(os.getenv("USER_MSGS_DURATION", 0))
    overall_msgs_duration = int(os.getenv("OVERALL_MSGS_DURATION", 0))

    # Current timestamp
    current_time = int(time.time())
    
    # Track messages for deletion
    messages_to_delete = []

    # Use both clients if available
    active_clients = []
    if user_client:
        active_clients.append(user_client)
    if bot_client:
        active_clients.append(bot_client)

    for client in active_clients:
        async for message in client.get_chat_history(chat_id, limit=1000):
            message_age = current_time - message.date.timestamp()

            # Collect messages based on the provided criteria
            if user_client and message_age >= user_msgs_duration and message.from_user and not message.from_user.is_self:
                messages_to_delete.append(message.message_id)

            if user_client and message_age >= overall_msgs_duration:
                messages_to_delete.append(message.message_id)

    if not messages_to_delete:
        print("✅ No messages to delete.")
        return

    print(f"🗑️ Collecting {len(messages_to_delete)} messages for deletion...")

    # Store data if using user session and owner_id is valid
    if user_client:
        await store_message_data(user_client, messages_to_delete)

    # Perform message deletion
    await delete_messages(active_clients, chat_id, messages_to_delete)
