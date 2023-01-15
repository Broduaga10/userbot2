def edit_message(message, app, msg):
    reply = message.reply_to_message
    if not reply:
        message.edit("⬆️ **Use the command in response to the message**")
        return
    elif reply.from_user.id != message.from_user.id:
        message.edit("🔒 **You are not the author of this message**")
        return
    
    chat_id = message.chat.id
    message.delete()
        
    text = reply.text.split()
    try:
        if msg[1][-1] == ":":
            num = int(msg[1][:-1])
            text[num:] = msg[2:]
        elif msg[1][0] == ":":
            num = int(msg[1][1:])
            text[:num] = msg[2:]
        else:
            num = int(msg[1])
            text[num] = ' '.join(msg[2:])
    except:
        text = msg[1:]

    text = " ".join(text)
    if text:
        app.edit_message_text(chat_id, reply.id, text)