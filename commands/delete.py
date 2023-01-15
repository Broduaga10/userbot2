from configparser import ConfigParser


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
                if message.from_user and \
                    message.from_user.id == user_id and message.id < message_id:
                    try:
                        app.edit_message_text(
                            chat_id=chat_id, message_id=message.id, text=dtext)
                    except:
                        messg = app.send_message(
                            chat_id=chat_id, text="**Can't edit**")
                        messg.edit(dtext)
                        app.delete_messages(chat_id=chat_id, message_ids=messg.id)
                    app.delete_messages(chat_id=chat_id, message_ids=message.id)
                    return
        else:
            try:
                app.edit_message_text(
                    chat_id=chat_id, message_id=message.reply_to_message_id, text=dtext)
            except: pass
            app.delete_messages(chat_id=chat_id, message_ids=message.reply_to_message_id)
    elif len(msg) <= 3:
        msg[1] = int(msg[1])
        if len(msg) > 2 and not msg[-1] in ["fast", "fst", "быстр", "бстр", "быстро"]:
            return
        message.edit(dtext)
        message.delete()

        msgid = message_id + msg[1]
        if message.reply_to_message:
            msgid = message.reply_to_message.id

        number = 0
        fast = not msg[-1] in ["fast", "fst", "быстр", "бстр", "быстро"]
        for message in app.get_chat_history(chat_id):
            if number < msg[1]:
                if message is not None and message.from_user.id == user_id and message.id <= msgid:
                    if fast:
                        try:
                            app.edit_message_text(
                                chat_id=chat_id, message_id=message.id, text=dtext)
                        except: pass
                    app.delete_messages(chat_id=chat_id, message_ids=message.id)
                    number += 1
            else:
                break