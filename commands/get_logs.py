from json import loads


def get_logs(message, msg, app):
    try:
        num = int(msg[1])
    except:
        num = 1

    result = ''
    try:
        for count, event in enumerate(app.get_chat_event_log(message.chat.id)):
            if count >= num:
                break
            action = str(event.action).split(".")[1]
            result += f'<pre>{action.lower()}</pre>'

            if action == "MESSAGE_DELETED":
                dm = event.deleted_message
                eu = event.user
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a> del " \
                            f"<a href=\"tg://user?id={dm.from_user.id}\">message</a> >\n{dm.text}\n"
            elif action == "MESSAGE_EDITED":
                om = event.old_message
                result += f"\n__{om.text}__ <a href=\"tg://user?id={om.from_user.id}\">></a> {event.new_message.text}\n"
            elif action == "DESCRIPTION_CHANGED":
                od = event.old_description
                if od == '':
                    od = "None"
                result += f"\n__{od}__ <a href=\"tg://user?id={event.user.id}\">></a>\n" \
                            f"{event.new_description}\n"
            elif action == "PHOTO_CHANGED":
                eu = event.user
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a> changed group photo\n"
            elif action == "TITLE_CHANGED":
                result += f"\n__{event.old_title}__ <a href=\"tg://user?id={event.user.id}\">></a>\n{event.new_title}\n"
            elif action == "MEMBER_INVITED":
                im = event.invited_member
                eu = event.user
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a>\n" \
                            f"invited <a href=\"tg://user?id={im.user.id}\">{im.user.username}</a>\n"
            elif action in ["MEMBER_JOINED", "MEMBER_LEFT"]:
                if action == "MEMBER_LEFT":
                    join_or_left = "left"
                else:
                    join_or_left = "joined"
                eu = event.user
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a> __{join_or_left}__\n"
            elif action in ["ADMINISTRATOR_PRIVILEGES_CHANGED", "MEMBER_PERMISSIONS_CHANGED"]:
                eu = event.user
                oap = event.old_administrator_privileges
                nap = event.new_administrator_privileges
                if action == "MEMBER_PERMISSIONS_CHANGED":
                    adm_or_member = 'member'
                else:
                    adm_or_member = 'admin'
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a> {adm_or_member} change privileges " \
                            f"<a href=\"tg://user?id={oap.user.id}\">{oap.user.username}</a> >\n"

                res_dict_oap = loads(str(oap.privileges))
                res_dict_nap = loads(str(nap.privileges))
                res = []
                for el in res_dict_nap:
                    if res_dict_oap[el] != res_dict_nap[el]:
                        res.append([el, res_dict_nap[el]])
                print(res)
                for el in res:
                    x = '-'
                    if el[1]:
                        x = '+'
                    result += f"__{x}{el[0]}__\n"
            elif action == "SLOW_MODE_CHANGED":
                result += f"\n__{event.old_slow_mode}__ <a href=\"tg://user?id={event.user.id}\">></a>\n{event.new_slow_mode}\n"
            elif action in ["MESSAGE_PINNED", "MESSAGE_UNPINNED"]:
                if action == "MESSAGE_PINNED":
                    pin = "pin"
                    pin_id = event.pinned_message.id
                else:
                    pin = "unpin"
                    pin_id = event.unpinned_message.id
                eu = event.user
                result += f"\n<a href=\"tg://user?id={eu.id}\">{eu.username}</a> {pin} " \
                            f"<a href=\"https://t.me/c/{str(message.chat.id)[3:]}/{pin_id}\">__message link__</a>\n"
            else:
                result += "__Just Nothing...__"
        try:
            message.edit(result)
        except:
            message.edit('📝 **The message text is too long**')
    except:
        message.edit('🔒 **No access to logs**')