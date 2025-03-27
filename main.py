import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Replace these with your own values
api_id = 0  # Your API ID (integer)
api_hash = ''  # Your API Hash (string)
session_string = ''  # Your session string for a user account

# Initialize the client with session string
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Store message IDs and their timestamps
message_tracker = {}

# Function to delete messages older than 24 hours
async def delete_old_messages(chat_id):
    now = datetime.now()
    async for message in client.iter_messages(chat_id):
        if message.date.replace(tzinfo=None) < now - timedelta(hours=24):
            try:
                await client.delete_messages(chat_id, message.id)
                logging.info(f"Deleted message {message.id} in chat {chat_id}")
            except Exception as e:
                logging.error(f"Failed to delete message {message.id}: {e}")

# Handler for new messages sent by the user
@client.on(events.NewMessage(outgoing=True))
async def handle_outgoing_message(event):
    chat_id = event.chat_id
    message_id = event.message.id
    sent_time = datetime.now()
    
    message_tracker[message_id] = sent_time
    
    await asyncio.sleep(24 * 3600)
    if message_id in message_tracker:
        try:
            await client.delete_messages(chat_id, message_id)
            logging.info(f"Deleted message {message_id} after 24 hours")
            del message_tracker[message_id]
        except Exception as e:
            logging.error(f"Failed to delete message {message_id}: {e}")

# Handler for the /rmrf command
@client.on(events.NewMessage(pattern='/rmrf'))
async def handle_rmrf(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    
    await event.respond("Deleting messages older than 24 hours...")
    await delete_old_messages(chat_id)
    await event.respond("Cleanup complete!")

# Start message on activation
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("User client started! I will delete my messages after 24 hours. Use /rmrf to delete all messages older than 24 hours.")

# Main function to run the client
async def main():
    await client.start()
    logging.info("User client is running...")
    await client.run_until_disconnected()

if name == 'main':
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
