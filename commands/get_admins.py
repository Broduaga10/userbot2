from pyrogram import enums


def get_admins(message, app):
    try:
        administrators = []
        for adm in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(adm)

        result = "<pre>🎖 Admins:</pre>"
        for i in range(len(administrators)):
            if str(administrators[i].status) == "ChatMemberStatus.OWNER":
                result += f"\n**Owner:** <a href=\"tg://user?id={administrators[i].user.id}\">" \
                            f"{administrators[i].user.username}</a>"
            else:
                result += f"\n**Admin:** <a href=\"tg://user?id={administrators[i].user.id}\">" \
                            f"{administrators[i].user.username}</a>"
        if result == "<pre>Admins:</pre>":
            result += "\n__**Empty**__"
        message.edit(result)
    except:
        message.edit("**Can't get admins**")
        return