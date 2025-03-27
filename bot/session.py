from pyrogram import Client

async def connect_user(api_id, api_hash, session_string):
    """
    Connect to Telegram using the User Session.
    """
    client = Client(
        name="user_session",
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string
    )
    await client.start()
    print("✅ User session connected successfully.")
    return client
