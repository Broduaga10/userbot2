import os.path
import shutil
from configparser import ConfigParser
from os import listdir

from pyrogram.raw.functions.contacts import ResolveUsername


def config():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config['DATA']['path']


def blacklist_user(message, msg, client, app):
    path = config()
    msg_text = message.text
    chat_id = message.chat.id
    
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
    elif len(msg) > 1 and msg[1][0] == '@':
        username = msg[1][1:]
    else:
        message.edit('❗️ **Wrong username** ❗️')
        return
    try:
        user_info = client.invoke(
            ResolveUsername(username=username)).users[0]
    except:
        message.edit('❗️ **This user does not exist** ❗️')
        return
    message.delete()

    uid = int(user_info.id)
    listdir = os.listdir(f'{path}/blacklist')


    if not str(uid) in listdir:
        os.mkdir(f"{path}/blacklist/{uid}")
        os.mkdir(f"{path}/blacklist/{uid}/files")
        if len(msg) > 2:
            if msg[1][0] == '@':
                text = ' '.join(msg_text.replace('\n', '%lb').split('@')[1].split()[1:])
            else:
                text = ' '.join(msg_text.replace('\n', '%lb').split()[2:])
        else:
            text = ''
        file = open(f"{path}/blacklist/{uid}/messages.txt", "w", encoding="utf-8")
        file.write(f"Text: {text}\n"); file.close()
        app.send_message(chat_id, f"🔇 <a href=\"https://t.me/{user_info.username}\">" \
                    f"{user_info.username}</a> - added to **blacklist**", disable_web_page_preview=True)
    else:
        shutil.rmtree(f"{path}/blacklist/{uid}")
        app.send_message(chat_id, f"🔈 <a href=\"https://t.me/{user_info.username}\">" \
                    f"{user_info.username}</a> - removed from **blacklist**", disable_web_page_preview=True)


def blacklist(message, app):
    path = config()

    try:
        uid = int(message.from_user.id)
    except: return

    if str(message.chat.type) == "ChatType.PRIVATE" and str(uid) in listdir(f'{path}/blacklist'):
        text_file = open(f"{path}/blacklist/{uid}/messages.txt", 'a+', encoding='UTF-8', errors='replace')

        if message.media is None or str(message.media) in ["MessageMediaType.WEB_PAGE", "MessageMediaType.CONTACT"]:
            text = str(message.date)[11:]+" "+message.from_user.username+" > "+message.text+"\n"
            file_extension = False
        elif str(message.media) == "MessageMediaType.PHOTO":
            file_extension = "jpg"
        elif str(message.media) == "MessageMediaType.VOICE":
            file_extension = "ogg"
        elif str(message.media) == "MessageMediaType.DOCUMENT":
            file_extension = f"{str(message.document.file_name).split('.')[-1]}"
        elif str(message.media) in ["MessageMediaType.VIDEO", "MessageMediaType.ANIMATION"]:
            file_extension = "MP4"
        else:
            file_extension = ""

        if file_extension:
            text = str(message.date)[11:]+" "+message.from_user.username+" > "+str(message.media)+"\n"
            app.download_media(message, f"{path}/blacklist/{uid}/files/{str(message.date)[11:].replace(':', '-')}.{file_extension}")

        file = open(f"{path}/blacklist/{uid}/messages.txt", "r", encoding='UTF-8', errors='replace')
        txt = file.readline().split("Text: ")[1].replace("%lb", "\n")
        
        try:
            app.send_message(message.chat.id, txt)
        except: pass
        message.delete()

        text_file.write(text)
        text_file.close()
