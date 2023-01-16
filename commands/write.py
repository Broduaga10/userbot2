from time import sleep

from pyrogram.errors import FloodWait


def write(message):
    name = ' '.join(message.text.split()[2:])

    if len(name) > 49:
        message.edit("**The message contains more than 50 characters, "
                    "in the process you will receive a temporary mute**")
        sleep(3)

    i = 0
    txt = ''
    while txt < name:
        try:
            message.edit(txt + "▒")
            txt += name[i]
            sleep(0.1)
            message.edit(txt)
            i += 1
        except FloodWait as e:
            sleep(e.value)
    try:
        message.edit(name)
    except: pass
