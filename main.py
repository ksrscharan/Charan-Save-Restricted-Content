import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json

# Load configuration from file
with open('config.json', 'r') as f:
    DATA = json.load(f)

def getenv(var):
    return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")

bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
acc = None

ss = getenv("STRING")
if ss is not None:
    acc = Client("myacc", api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()

# Add proper exit condition to loops
def wait_and_remove_file(filepath):
    time.sleep(3)
    while os.path.exists(filepath):
        with open(filepath, "r") as file:
            txt = file.read()
        try:
            os.remove(filepath)  # Remove file at the end
            break  # Exit loop once file is removed
        except Exception as e:
            print(f"Error while removing file: {e}")
        time.sleep(5)

# Proper error handling and file closing
def edit_message_safe(chat_id, message_id, text):
    try:
        bot.edit_message_text(chat_id, message_id, text)
    except Exception as e:
        print(f"Error editing message: {e}")

# ... (Other functions remain unchanged) ...

# Use this pattern for start command
@bot.on_message(filters.command(["start"]))
def send_start(client, message):
    try:
        bot.send_message(
            message.chat.id,
            f"**👋 Hi** **{message.from_user.mention}**, **I am Save Restricted Bot, I can send you restricted content by its post link**\n\n{USAGE}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🌐 Update Channel", url="https://t.me/dummylazey")]]
            ),
            reply_to_message_id=message.id,
        )
    except Exception as e:
        print(f"Error in start command: {e}")

# ... (Other functions remain unchanged) ...

# Implement proper error handling and file management in the handle_private function
def handle_private(message, chat_id, msg_id):
    try:
        msg = acc.get_messages(chat_id, msg_id)
        msg_type = get_message_type(msg)
        # ... (Handle message types) ...
        os.remove(file)  # Remove downloaded file
        if os.path.exists(f'{message.id}upstatus.txt'):
            os.remove(f'{message.id}upstatus.txt')
        bot.delete_messages(message.chat.id, [smsg.id])
    except Exception as e:
        print(f"Error handling private message: {e}")

# ... (Other functions remain unchanged) ...

USAGE = """**FOR PUBLIC CHATS**
... (Your usage instructions) ...
"""

# Use try-except to handle unexpected errors during bot execution
try:
    bot.run()
except Exception as e:
    print(f"Bot execution error: {e}")
