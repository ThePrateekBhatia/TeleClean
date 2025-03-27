# 📢 TeleClean

A **powerful** and **efficient** script using the **Telethon** Python library to connect with **Telegram** and automatically clean your chats in **groups** and **supergroups**. It deletes your messages after 24 hours and allows bulk deletion of older messages on demand.

## ✨ Features

- **Auto-Delete Messages** – Automatically deletes your outgoing messages after 24 hours.
- **Bulk Cleanup** – Use the `/rmrf` command to delete all messages older than 24 hours.
- **Group & Supergroup Support** – Works seamlessly across all Telegram chat types.
- **Customizable** – Modify retention time or target specific chats easily.
- **Lightweight & Fast** – Efficient message handling with real-time logging.

## 📦 Requirements

- Python 3.8+
- Telethon library
- Telegram API credentials (API ID, API Hash, and a session string)

## 🚀 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/TeleClean.git
cd TeleClean
```

2. **Set Up Environment**

Ensure you have Python and **Telethon** installed:

```bash
pip install -r requirements.txt
```

3. **Generate Session String**

Use the provided script in the `assets` folder to generate your session string:

```bash
python assets/generate_session.py
```

Your session string will be sent to your **Saved Messages** with the tags `#SessionString #Telethon #TeleClean`.

4. **Configure the Script**

Open the script and replace the following placeholders:

```python
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
session_string = 'YOUR_SESSION_STRING'
```

## ▶️ Usage

1. **Run the Script**

```bash
python main.py
```

2. **Commands**

- `/start` – Initialize the bot and display a welcome message.
- `/rmrf` – Delete all messages older than 24 hours in the current chat.

## 🔧 Customization

- **Change Auto-Delete Time** – Modify the time window by updating this line:

```python
await asyncio.sleep(24 * 3600)  # 24 hours
```

- **Target Specific Chats** – Filter specific chats by adding conditions in the `handle_outgoing_message` function.

## 📜 License

This project is licensed under the MIT License. Feel free to modify and distribute it.

## 📞 Support

For issues or questions, open an [issue](https://github.com/yourusername/TeleClean/issues) or contribute via a pull request!

