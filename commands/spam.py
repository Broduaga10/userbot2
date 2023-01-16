from time import sleep


def spam(message, app, msg):
    chat_id = message.chat.id

    reply = None
    if message.reply_to_message is not None:
        reply = message.reply_to_message_id
    try:
        num = int(msg[1])

        text = []
        if len(message.text.split('\n')) > 1:
            for i in message.text.split('\n'):
                text.append(i)
        elif len(message.text.split()) > 3:
            text.append(message.text)
        elif len(message.text.split()) < 3:
            message.edit("⚠️ **Write a text for spam**")
            return
        else:
            message.edit("⚠️ **Write a text for spam**")
            return
        text[0] = ' '.join(text[0].split()[3:])
        message.delete()

        autodel = False
    except ValueError:
        try:
            num = int(msg[2])
            if message.text.split()[2] in ['silent', 'бесшумн', 'бсшм']:
                text = []
                if len(message.text.split('\n')) > 1:
                    for i in message.text.split('\n'):
                        text.append(i)
                elif len(message.text.split()) > 4:
                    text.append(message.text)
                else:
                    message.edit("⚠️ **Write a text for spam**")
                    return

                text[0] = ' '.join(text[0].split()[4:])
                message.delete()

                autodel = True

            elif message.text.split()[2] in ['num', 'numbers', 'числа', 'числ', 'цифры']:
                message.delete()
                for i in range(num):
                    app.send_message(chat_id, i+1, reply_to_message_id=reply)

                mesg = app.send_message(chat_id, "**Done!** ✅")
                sleep(0.3)
                app.delete_messages(chat_id, mesg.id)
                return

            else:
                message.edit("⚠️ **Wrong argument**")
                return
        except:
            message.edit("⚠️ **Write number of iterations**")
            return
    except:
        message.edit("⚠️ **Write number of iterations**")
        return

    text = '\n'.join(text)
    for i in range(num):
        mesg = app.send_message(chat_id, text, reply_to_message_id=reply)
        if autodel:
            app.delete_messages(chat_id, mesg.id)

    mesg = app.send_message(chat_id, "**Done!** ✅")
    sleep(0.3)
    app.delete_messages(chat_id, mesg.id)