from random import choice


def role_play(message, app, msg):
    next_text = ""
    if len(message.text.split("\n")) > 1:
        x = msg.index(message.text.split("\n")[0].split()[-1])+1
        msg = msg[:x]
        next_text = message.text.split("\n")[1]

    if message.reply_to_message:
        reply_id = message.reply_to_message.id
        if msg[-1][0] == "@":
            username = message.reply_to_message.from_user.username
            username2 = msg[-1][1:]
            action = " ".join(msg[1:-1])
        else:
            username = message.from_user.username
            username2 = message.reply_to_message.from_user.username
            action = " ".join(msg[1:])
    else:
        reply_id = None
        try:
            if msg[1][0] == "@" and msg[-1][0] == "@":
                username = msg[1][1:]
                username2 = msg[-1][1:]
                action = " ".join(msg[2:-1])
            elif msg[-1][0] == "@":
                username = message.from_user.username
                username2 = msg[-1][1:]
                action = " ".join(msg[1:-1])
            elif msg[1][0] == "@":
                username = msg[1][1:]
                username2 = message.from_user.username
                action = " ".join(msg[2:])
        except:
            message.delete()
            app.send_message(message.chat.id, '**Wrong username**')
            return
    message.delete()

    emojis = ['π', 'π', 'π', 'π', 'π₯Ή', 'π', 'π€£', 'π₯²', 'βΊοΈ', 'π', 'π', 'π', 'π',
            'π', 'π', 'π', 'π₯°', 'π', 'π', 'π', 'π€ͺ', 'π€¨', 'π§', 'π', 'π€©','π',
            'π', 'π', 'π£', 'π₯Ί', 'π’', 'π­', 'π€', 'π‘', 'π€¬', 'π€―', 'π³', 'π₯΅', 'π₯Ά',
            'π±', 'π°', 'π', 'π€', 'π€', 'π«£', 'π€­', 'π«‘', 'π€₯', 'πΆ', 'π', 'π', 'π¬',
            'π', 'π§', 'π₯±', 'π΄', 'π€€', 'πͺ', 'π΅', 'π₯΄', 'π€§', 'π€', 'π', 'π»', 'β οΈ', 
            'πΎ', 'π«Ά', 'π€²', 'π', 'π', 'π', 'π€', 'π', 'π', 'β' 'π€', 'βοΈ', 'π€', 
            'π', 'π€', 'π€', 'βοΈ', 'π€', 'πͺ', 'π', 'π§ ', 'π£', 'π', 'π«', 'π', 'π',
            'π', 'π«', 'β­οΈ', 'β¨', 'π₯', 'π¨', 'π¦', 'π', 'π', 'π', 'π«', 'π£', 'π§¨', 
            'πͺ', 'πͺ', 'π?', 'π½', 'π', 'β€οΈ', 'π€', 'π€', 'π', 'β€οΈβπ₯', 'β€οΈβπ©Ή', 'β', 'βοΈ', 
            'βοΈ', 'βΏοΈ']

    user_info = f"<a href=\"https://t.me/{username}\">{username}</a>"
    user_info2 = f"<a href=\"https://t.me/{username2}\">{username2}</a>"
    result = choice(emojis) + f" | {user_info} {action} {user_info2} " + next_text


    app.send_message(message.chat.id, result, reply_to_message_id=reply_id, disable_web_page_preview=True)