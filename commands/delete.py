from configparser import ConfigParser
from json import loads
from os import path, remove


def config(bool):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    if bool:
        return config['DATA']['path']
    else:
        return config['DATA']['delete_text']
    

def delete(message, msg, app):
    dtext = config(False)

    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.id

    if len(msg) == 1:
        message.edit(dtext)
        message.delete()
        if message.reply_to_message is None:
            for message in app.get_chat_history(chat_id):
                if message and \
                    message.from_user.id == user_id and message.id < message_id:
                    try:
                        app.edit_message_text(
                            chat_id=chat_id, message_id=message.id, text=dtext)
                    except: pass
                    app.delete_messages(chat_id=chat_id, message_ids=message.id)
                    return
        else:
            try:
                app.edit_message_text(
                    chat_id=chat_id, message_id=message.reply_to_message_id, text=dtext)
            except: pass
            try:
                app.delete_messages(chat_id=chat_id, message_ids=message.reply_to_message_id)
            except:
                app.send_message(chat_id, "**Can't delete message**")
    elif len(msg) <= 3:
        try:
            msg[1] = int(msg[1])
        except: return
        
        if len(msg) > 2 and not msg[-1] in ["fast", "fst", "быстр", "бстр", "быстро"]:
            return
        message.edit(dtext)
        message.delete()

        msgid = message_id + msg[1]
        if message.reply_to_message:
            msgid = message.reply_to_message.id

        number = 0
        fast = msg[-1] in ["fast", "fst", "быстр", "бстр", "быстро"]
        for message in app.get_chat_history(chat_id):
            if number < msg[1]:
                if message and message.from_user.id == user_id and message.id <= msgid:
                    if not fast:
                        try:
                            app.edit_message_text(
                                chat_id=chat_id, message_id=message.id, text=dtext)
                        except: pass
                    app.delete_messages(chat_id=chat_id, message_ids=message.id)
                    number += 1
            else:
                break


def delete_message(message):
    path = config(True)

    name = ' '.join(message.text.split()[2:])
    
    read = open(f'{path}/message.txt', 'r',
                    encoding='UTF-8', errors='replace')
    lines = read.readlines()
    read.close()

    print("name - "+name)
    x = True
    result = ""
    for line in lines:
        dictionary = loads(line)
        if dictionary["name"] == name:
            x = False
            continue
        print(dictionary["name"])
        result += line
    if x:
        message.edit(f"⚠️ **No such text in file**")
        return

    write = open(f'{path}/message.txt', 'w',
                    encoding='UTF-8', errors='replace')
    write.write(result)
    write.close()
    message.edit(f"✅ **Done!**\nText has been removed")


def delete_photo(message):
    path1 = config(True)
    name = ' '.join(message.text.split()[2:])
    try:
        remove(path.join(path.abspath(path.dirname(f'{path1}\\photo\\')), f'{name}.jpg'))
        message.edit(
            f"✅ **Done!**\nFile __{name}.jpg__ has been deleted")
    except:
        message.edit("⚠️ **This title is not in the list**")


def delete_video(message):
    path1 = config(True)
    name = ' '.join(message.text.split()[2:])
    try:
        remove(path.join(path.abspath(path.dirname(f'{path1}\\video\\')), f'{name}.mp4'))
        message.edit(
            f"✅ **Done!**\nFile __{name}.mp4__ has been deleted")
    except:
        message.edit("⚠️ **This title is not in the list**")


def delete_voice_message(message):
    path1 = config(True)
    name = ' '.join(message.text.split()[2:])
    try:
        remove(path.join(path.abspath(path.dirname(f'{path1}\\voice\\')), f'{name}.ogg'))
        message.edit(
            f"✅ **Done!**\nFile __voice\\{name}.ogg__ has been deleted")
    except:
        message.edit("⚠️ **This title is not in the list**")
