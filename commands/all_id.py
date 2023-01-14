def all_id(message):
    r = message.reply_to_message
    reply = False
    if r is not None:
        reply = True

    result = '🆔 <pre>All ID</pre>\n\n' \
                f'**Your ID:** `{message.from_user.id}`\n'
    if reply:
        result += f'**User Reply ID:** `{r.from_user.id}`\n'

    result += f'**Message ID:** `{message.id}`\n'
    if reply:
        result += f'**Message Reply ID:** `{r.id}`\n'

    if str(message.chat.type).split('.')[1] in ['SUPERGROUP', 'GROUP']:
        result += f'**Chat ID:** `{message.chat.id}`'

    message.edit(result)