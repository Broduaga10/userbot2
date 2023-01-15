import os.path
import shutil
from configparser import ConfigParser

from pyrogram.raw.functions.contacts import ResolveUsername


def blacklist(message, msg, client, app):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    path = config['DATA']['path']
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