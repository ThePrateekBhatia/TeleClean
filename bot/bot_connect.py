from pyrogram import Client

async def connect_bot(api_id, api_hash, bot_token):
    """
    Connect to Telegram using the Bot Token.
    """
    client = Client(
        name="bot_client",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token
    )
    await client.start()
    print("✅ Bot token connected successfully.")
    return client
