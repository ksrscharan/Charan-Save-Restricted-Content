import re
import pyrogram # You need to import the pyrogram module

# You need to define the acc variable and assign it a Client object
acc = pyrogram.Client("my_account")

@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    print(message.text)

    # joining chats
    chat_link_pattern = r"https?://t\.me/[a-zA-Z0-9_]+"
    chat_links = re.findall(chat_link_pattern, message.text)

    if len(chat_links) > 0:
        if acc is None:
            bot.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
            return

        for chat_link in chat_links:
            try:
                # You need to use the acc variable instead of the client parameter
                acc.join_chat(chat_link)
                bot.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
            except UserAlreadyParticipant:
                bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
            except InviteHashExpired:
                bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)
            except Exception as e: # You need to handle other possible exceptions
                bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)
                return

    # ...
