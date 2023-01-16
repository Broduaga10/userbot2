from configparser import ConfigParser
from json import loads
from os import listdir
from os.path import exists


def config():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config


def save_new_message(message):
    path = config()['DATA']['path']
    name = ' '.join(message.text.split()[2:])

    reply = message.reply_to_message
    if reply is None:
        message.edit("**Use the command in response to the message** ⤴️")
        return
    elif name == '':
        message.edit(f"✏️ **Enter the title**")
        return
    elif set(list(name)) & {'\\', '"'}:
            message.edit(f"⚠️ **Forbidden character in title:**\n(\\) or (\")")
            return
    elif set(list(reply.text)) & {'\\', '"'}:
            message.edit(f"⚠️ **Forbidden character in text:**\n(\\) or (\")")
            return

    if not reply.media or reply.caption or str(reply.media) in ["MessageMediaType.WEB_PAGE", "MessageMediaType.CONTACT"] :
        read = open(f'{path}/message.txt', 'r',
                    encoding='UTF-8', errors='replace')
        lines = read.readlines()
        read.close()

        for line in lines:
            dictionary = loads(line)
            if dictionary["name"] == name:
                message.edit(f"❌ **Note with the same name already exists**")
                return
        
        try:
            result = ''
            for i in reply.text.split('\n'):
                result += i + '%lb'
        except:
            result = ''
            for i in reply.caption.split('\n'):
                result += i + '%lb'

        result = str({
            "name": name,
            "text": result,
            "author": {
                "first_name": reply.from_user.first_name,
                "username": reply.from_user.username,
                "user_id": reply.from_user.id,
                "chat_title": reply.chat.title,
                "date": str(reply.date)
            }
        }).replace("'", '"')

        file = open(f'{path}/message.txt', 'a',
                    encoding='UTF-8', errors='replace')
        file.write(f'{result}\n')
        file.close()

        message.edit(f"**Done!** ✅\nTitle - `{name}`")
        return


def save_new_photo(message, app):
    path = config()['DATA']['path']
    name = ' '.join(message.text.split()[2:])

    reply = message.reply_to_message
    if str(reply.media) == "MessageMediaType.PHOTO":
        if exists(f'{path}/photo/{name}.jpg'):
            message.edit(f"❌ **File with this name already exists**")
            return
        if set(list(name)) & {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}:
            message.edit(f"⚠️ **Forbidden character in title:**\n\ / : * ? \" < > |")
            return

        try:
            path1 = f'{path}/photo/{name}.jpg'
            app.download_media(reply, file_name=path1)
            message.edit(f"**Done! ✅**\nTitle - `{name}`")
        except: 
            message.edit('‼️ **ERROR DOWNLOAD** ‼️')


def save_new_video(message, app):
    path = config()['DATA']['path']
    name = ' '.join(message.text.split()[2:])

    reply = message.reply_to_message
    if str(reply.media) == "MessageMediaType.VIDEO":
        if exists(f'{path}/video/{name}.MP4'):
            message.edit(f"❌ **File with this name already exists**")
            return
        if set(list(name)) & {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}:
            message.edit(f"⚠️ **Forbidden character in title:**\n\ / : * ? \" < > |")
            return

        try:
            path1 = f'{path}/video/{name}.MP4'
            message.edit(f"⏳ __Downloading the video...__\n📥 **{round(reply.video.file_size/1048576, 3)} MB**")
            app.download_media(reply, file_name=path1)
            message.edit(f"**Done! ✅**\nTitle - `{name}`")
        except: 
            message.edit('‼️ **ERROR DOWNLOAD** ‼️')


def save_new_voice_message(message, app):
    path = config()['DATA']['path']
    name = ' '.join(message.text.split()[2:])

    reply = message.reply_to_message
    if str(reply.media) == "MessageMediaType.VOICE":
        if exists(f'{path}/voice/{name}.ogg'):
            message.edit(f"❌ **File with this name already exists**")
            return
        if set(list(name)) & {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}:
            message.edit(f"⚠️ **Forbidden character in title:**\n\ / : * ? \" < > |")
            return

        try:
            path1 = f'{path}/voice/{name}.ogg'
            app.download_media(reply, file_name=path1)
            message.edit(f"**Done! ✅**\nTitle - `{name}`")
        except: 
            message.edit('‼️ **ERROR DOWNLOAD** ‼️')
