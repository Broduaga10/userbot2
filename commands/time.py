def time(message):
    result = 'š° **Time:** ' + str(message.date)
    if message.reply_to_message:
        result += '\nš° **Send time:** ' + str(message.reply_to_message.date)
        if message.reply_to_message.edit_date:
            result += '\nš° **Edit time:** ' + str(message.reply_to_message.edit_date)
    
    message.edit(result)