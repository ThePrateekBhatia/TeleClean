import aiohttp
import asyncio
import datetime

async def save_to_spacebin(content):
    """
    Uploads deleted messages to spaceb.in and returns the link.

    Args:
    - content (str): Text content to be uploaded.

    Returns:
    - str: URL of the uploaded content or None on failure.
    """
    url = "https://spaceb.in/api/v1/documents"
    data = {"content": content, "extension": "txt"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return f"https://spaceb.in/{result['payload']['id']}"
            print(f"❌ Failed to upload to spaceb.in: {response.status}")
            return None

async def collect_message_data(messages):
    """
    Formats messages into a readable text for saving.

    Args:
    - messages (list): List of message objects.

    Returns:
    - str: Formatted message log.
    """
    log = f"🗓️ Deleted Messages (Collected on {datetime.datetime.now()}):\n\n"
    for msg in messages:
        time = msg.date.strftime("%Y-%m-%d %H:%M:%S")
        user = msg.from_user.first_name if msg.from_user else "Unknown"
        content = msg.text or msg.caption or "[Media Message]"
        log += f"[{time}] {user}: {content}\n"
    return log

async def handle_deleted_data(client, messages, owner_id):
    """
    Handles storage of deleted messages (uploads or sends to owner's PM).

    Args:
    - client: Pyrogram client.
    - messages (list): List of deleted messages.
    - owner_id (int): Telegram ID of the bot owner.
    """
    if not messages:
        return

    message_data = await collect_message_data(messages)

    # Upload to spaceb.in
    link = await save_to_spacebin(message_data)

    # Send data to the owner's saved messages
    if owner_id:
        if link:
            await client.send_message(owner_id, f"🔗 Deleted Messages Log: {link}")
        else:
            filename = f"deleted_messages_{datetime.datetime.now():%Y%m%d}.txt"
            await client.send_document(owner_id, filename=filename, file_content=message_data)
        print("✅ Sent deleted messages to the owner's PM.")
