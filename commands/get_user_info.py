from json import loads

from pyrogram.raw.functions.contacts import ResolveUsername


def get_user_info(message, msg, client):
    if message.reply_to_message:
        username = message.reply_to_message.from_user.username
    elif len(msg) > 1 and msg[1][0] == '@':
        username = msg[1][1:]
    else:
        message.edit('❗️ **Wrong username** ❗️')
        return
    try:
        user_info = client.get_chat_member(message.chat.id, 
                                            client.invoke(
                                                ResolveUsername(username=username)).peer.user_id)
    except:
        try:
            user_info = client.invoke(
                ResolveUsername(username=username)).users[0]
        except:
            message.edit('❗️ **This user does not exist** ❗️')
            return
    res_dict = loads(str(user_info))

    if str(user_info.status).split('.')[1] in ["MEMBER", "OWNER", "ADMINISTRATOR", "RESTRICTED"]:
        result = f"<pre>User:</pre>\n**Name:** <a href=\"tg://user?id={user_info.user.id}\">" \
                    f"{user_info.user.first_name}</a>" \
                    f"\n**Username:** {user_info.user.username}" \
                    f"\n**ID:** {user_info.user.id}" \
                    f"\n**Premium:** {user_info.user.is_premium}" \
                    f"\n**Contact:** {user_info.user.is_contact}"

        if user_info.promoted_by is not None:
            result += "\n\n<pre>Restricted by:</pre>" \
                        f"\n**Name:** <a href=\"tg://user?id={user_info.promoted_by.id}\">" \
                        f"{user_info.promoted_by.first_name}</a>" \
                        f"\n**Username:** {user_info.promoted_by.username}" \
                        f"\n**ID:** {user_info.promoted_by.id}"

        if user_info.privileges is not None:
            result += f"\n\n<pre>Chat Permissions:</pre>" \
                        f"\n**Status:** {str(user_info.status).split('.')[1].lower()}" \
                        f"\n**Send messages:** {user_info.privileges.can_post_messages}" \
                        f"\n**Change info:** {user_info.privileges.can_change_info}" \
                        f"\n**Promote members:** {user_info.privileges.can_promote_members}" \
                        f"\n**Invite users:** {user_info.privileges.can_invite_users}" \
                        f"\n**Pin messages:** {user_info.privileges.can_pin_messages}"

    elif str(message.chat.type).split('.')[1] == 'PRIVATE':
        result = f"<pre>User:</pre>\n**Name:** <a href=\"https://t.me/{res_dict['username']}\">" \
                    f"{res_dict['first_name']}</a>" \
                    f"\n**Username:** {res_dict['username']}" \
                    f"\n**ID:** {res_dict['id']}" \
                    f"\n**Premium:** {res_dict['premium']}" \
                    f"\n**Contact:** {res_dict['contact']}"
        try:
            if not msg[-1] in ['nophone', 'hide', 'hidden', 'скрыть']:
                result += f"\n**Phone Number:** ||{res_dict['phone']}||"
            else:
                result += f"\n**Phone Number:** ||hidden||"
        except:
            result += f"\n**Phone Number:** ||hidden||"

    elif res_dict["_"].split('.')[1] == "User":
        result = f"<pre>User:</pre>\n**Name:** <a href=\"tg://user?id={res_dict['id']}\">" \
                    f"{res_dict['first_name']}</a>" \
                    f"\n**Username:** {res_dict['username']}" \
                    f"\n**ID:** {res_dict['id']}" \
                    f"\n**Premium:** {res_dict['premium']}" \
                    f"\n**Contact:** {res_dict['contact']}"

    message.edit(result, disable_web_page_preview=True)