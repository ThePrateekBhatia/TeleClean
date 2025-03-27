import aiohttp
import asyncio
from datetime import datetime

async def save_messages(messages, owner_client, owner_id):
    """
    Saves messages and sends them to the owner via PM or a paste service.

    Args:
    - messages (list): List of messages to save.
    - owner_client: Client to send the saved data (user session).
    - owner_id (int): Telegram ID of the owner.
    """
    if not messages:
        print("⚠️ No messages to save.")
        return

    # Format messages for storage
    data = "\n\n".join(
        f"[{msg.date.strftime('%Y-%m-%d %H:%M:%S')}] {msg.sender_id}: {msg.text}"
        for msg in messages if msg.text
    )

    # Create filename with current timestamp
    filename = f"deleted_msgs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Save to local file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

    # Upload to paste service (spaceb.in)
    paste_url = await upload_to_paste(data)

    # Send results to the owner
    if owner_client:
        try:
            # Send both the file and the paste link
            await owner_client.send_message(owner_id, f"🗑️ Deleted Messages Log:\n{paste_url}")
            await owner_client.send_document(owner_id, filename)
            print(f"✅ Messages sent to owner: {owner_id}")
        except Exception as e:
            print(f"❌ Error sending data to owner: {e}")

async def upload_to_paste(data):
    """
    Uploads data to spaceb.in and returns the paste link.

    Args:
    - data (str): Content to upload.

    Returns:
    - str: Paste URL or error message.
    """
    url = "https://spaceb.in/api/v1/documents/"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"content": data, "extension": "txt"}) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return f"https://spaceb.in/{result['payload']['id']}"
                else:
                    print(f"❌ Failed to upload to spaceb.in: {resp.status}")
                    return "Failed to upload logs."
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return "Error uploading logs."
