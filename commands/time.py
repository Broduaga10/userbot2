def time(message):
    result = '🕰 **Time:** ' + str(message.date)
    if message.reply_to_message:
        result += '\n🕰 **Send time:** ' + str(message.reply_to_message.date)
        if message.reply_to_message.edit_date:
            result += '\n🕰 **Edit time:** ' + str(message.reply_to_message.edit_date)
    
    message.edit(result)