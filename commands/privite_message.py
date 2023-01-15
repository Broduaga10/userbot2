from pyrogram.raw.functions.contacts import ResolveUsername


def privite_message(message, app, msg, client):
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
        text = " ".join(msg[1:])
    elif not len(msg) < 1:
        if msg[1][0] == "@":
            username = msg[1][1:]
            text = " ".join(msg[2:])
        elif msg[-1][0] == "@":
            username = msg[-1][1:]
            text = " ".join(msg[1:-1])
    else:
        message.edit("❗️ **User not found** ❗️")
        return

    try:
        user_info = client.invoke(
            ResolveUsername(username=username)).users[0]
    except:
        message.edit('❗️ **This user does not exist** ❗️')
        return
    uid = int(user_info.id)
        
    try:
        app.send_message(uid, text)
        message.edit(f"<a href=\"https://t.me/{user_info.username}\">" \
                    f"Done!</a>", disable_web_page_preview=True)
    except: pass