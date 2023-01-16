from json import loads
from pyrogram.raw.functions.contacts import ResolveUsername
from configparser import ConfigParser


def config():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config


def trust_user(message, msg, client, app):
    path = config()['DATA']['path']

    file = open(f"{path}/trusted.txt", 'r', encoding='UTF-8', errors='replace')
    trusted = loads(file.readline())
    file.close()

    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
    elif len(msg) > 1:
        if msg[1][0] == "@":
            username = msg[1][1:]
        elif msg[-1][0] == "@":
            username = msg[-1][1:]
    
    try:
        user_info = client.invoke(ResolveUsername(username=username)).users[0]
        uid = int(user_info.id)
    except: pass

    if msg[0][0] == "+":
        if not uid in trusted:
            trusted.append(uid)
            message.edit(f"🔓 **You trust the user:** " \
                         f"<a href=\"https://t.me/{username}\">{username}</a>",
                         disable_web_page_preview=True)
        else:
            message.edit("🔓 **This user is already in the list**")
            return
    elif msg[0][0] == "-":
        if uid in trusted:
            trusted.remove(uid)
            message.edit(f"🔒 **You don't trust the user:** " \
                         f"<a href=\"https://t.me/{username}\">{username}</a>",
                         disable_web_page_preview=True)
        else:
            message.edit("❌ **This user is not in the list**")
            return
    else:
        result = '🔐 **Trusted users:**\n'
        for uid in trusted:
            try:
                user = app.get_chat_member(chat_id=message.chat.id, user_id=uid)
            except:
                user = False
            if user:
                result += f"- <a href=\"https://t.me/{user.user.username}\">{user.user.username}</a>\n"
            elif message.chat.id == uid:
                result += f"- This user"
            else:
                result += f"- __failed__ ({uid})\n"
        message.edit(result, disable_web_page_preview=True)

    if msg[0][0] in ["+", "-"]:
        write = open(f"{path}/trusted.txt", 'w', encoding='UTF-8', errors='replace')
        write.write(str(trusted))
        write.close()


def trust(message, app):
    path = config()['DATA']['path']
    prefix = config()['PREFIXES']['prefix']

    try:
        uid = int(message.from_user.id)
    except: return

    file = open(f"{path}/trusted.txt", 'r', encoding='UTF-8', errors='replace')
    trusted = loads(file.readline())
    file.close()
    comm = ["write", "type", "напиши", "скажи", "ответь", "пиши"]
    if uid in trusted \
        and message.text \
            and message.text.split()[0].lower() in prefix \
                and message.text.split()[1].lower() in comm:
            
        try: message.delete()
        except: pass

        reply = None
        if message.reply_to_message:
            reply = message.reply_to_message_id

        text = " ".join(message.text.split(" ")[2:])
        if text:
            app.send_message(message.chat.id, text, reply_to_message_id=reply)
