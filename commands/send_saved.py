from json import loads
from configparser import ConfigParser
from os.path import getsize


def config():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config


def send_saved_message(message, msg):
    path = config()['DATA']['path']

    read = open(f'{path}/message.txt', 'r', encoding='UTF-8', errors='replace')
    lines = read.readlines()
    read.close()

    name = ' '.join(message.text.split()[2:])

    author = False
    if msg[-1].lower() in ["author", "ath", "автор", "авт", "from", "user"]:
        author = True

    for line in lines:
        dictionary = loads(line)

        if author:
            if dictionary['name'] == " ".join(name.split()[:-1]):
                author = dictionary['author']

                if author['chat_title'] == 'None':
                    author['chat_title'] = 'private'

                result = f"<pre>Author</pre>\n" \
                            f"**First name:** {author['first_name']}\n" \
                            f"**Username:** [{author['username']}](https://t.me/{author['username']})\n" \
                            f"**User ID:** {author['user_id']}\n" \
                            f"**Chat:** {author['chat_title']}\n" \
                            f"**Date:** {author['date'].split()[0]}\n" \
                            f"**Time:** {author['date'].split()[1]}"
                break
            
        elif dictionary['name'] == name:
            result = ''
            for i in dictionary['text'].split("%lb"):
                result += i + '\n'
            break
    else:
        message.edit("⚠️ **This title is not in the list**")
        return

    message.edit(result, disable_web_page_preview=True)


def send_saved_photo(message, app):
    chat_id = message.chat.id
    name = ' '.join(message.text.split()[2:])
    message.delete()
    path = config()['DATA']['path']

    reply = None
    if message.reply_to_message is not None:
        reply = message.reply_to_message_id

    try:
        app.send_photo(
            chat_id, f'{path}/photo/{name}.jpg', reply_to_message_id=reply)
    except ValueError:
        app.send_message(chat_id, "⚠️ **This title is not in the list**")


def send_saved_video(message, app):
    path = config()['DATA']['path']
    chat_id = message.chat.id
    name = ' '.join(message.text.split()[2:])

    reply = None
    if message.reply_to_message is not None:
        reply = message.reply_to_message_id

    try:
        file_size = round(getsize(f'{path}/video/{name}.MP4')/1048576, 3)
        message.edit(f"⏳ __Uploading the video...__\n📤 **{file_size} MB**")
        app.send_video(
            chat_id, f'{path}/video/{name}.MP4', reply_to_message_id=reply)
        message.delete()
    except: 
        message.edit("⚠️ **This title is not in the list**")


def send_saved_voice_message(message, app):
    chat_id = message.chat.id
    name = ' '.join(message.text.split()[2:])
    message.delete()
    path = config()['DATA']['path']
    
    reply = None
    if message.reply_to_message is not None:
        reply = message.reply_to_message_id

    try:
        app.send_voice(
            chat_id, f'{path}/voice/{name}.ogg', reply_to_message_id=reply)
    except:
        app.send_message(chat_id, "⚠️ **This title is not in the list**")