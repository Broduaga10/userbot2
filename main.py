from pyrogram import Client, filters
from configparser import ConfigParser
from ast import literal_eval
from commands import *


def get_cfg():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config

config = get_cfg()
api_id = int(config['API']['api_id'])
api_hash = config['API']['api_hash']

app = Client("my_account", api_id=api_id, api_hash=api_hash)


@app.on_message(filters.me)
def main(client, message):
    config = get_cfg()
    prefix = literal_eval(config['PREFIXES']['prefix'])
    dprefix = literal_eval(config['PREFIXES']['delete_prefix'])
    def get_command(command):
        return literal_eval(config['COMMANDS'][command])

    try:
        msg = message.text.split()
    except: return

    if msg[0] in prefix:
        msg = msg[1:]
    elif msg[0][0] in prefix:
        msg[0] = msg[0][1:]
    elif msg[0] in dprefix:
        delete(message, msg, app)
        return
    elif len(msg) < 2: return
    else: return

    command = msg[0]
    if command in get_command('all_id'):
        all_id(message)
    elif command in get_command('blacklist'):
        blacklist_user(message, msg, client, app)
    elif command in get_command('config'):
        cfg(message, msg)
    elif command in get_command('delete_message'):
        delete_message(message)
    elif command in get_command('delete_photo'):
        delete_photo(message)
    elif command in get_command('delete_video'):
        delete_video(message)
    elif command in get_command('delete_voice_message'):
        delete_voice_message(message)
    elif command in get_command('edit_message'):
        edit_message(message, app, msg)
    elif command in get_command('get_admins'):
        get_admins(message, app)
    elif command in get_command('get_logs'):
        get_logs(message, msg, app)
    elif command in get_command('get_saved_messages'):
        get_saved_messages(message)
    elif command in get_command('get_saved_photos'):
        get_saved_photos(message)
    elif command in get_command('get_saved_videos'):
        get_saved_videos(message)
    elif command in get_command('get_saved_voice_messages'):
        get_saved_voice_messages(message)
    elif command in get_command('get_user_info'):
        get_user_info(message, msg, client)
    elif command in get_command('ping'):
        ping(message, msg)
    elif command in get_command('privite_message'):
        privite_message(message, app, msg, client)
    elif command in get_command('role_play'):
        role_play(message, app, msg)
    elif command in get_command('save_new_message'):
        save_new_message(message)
    elif command in get_command('save_new_photo'):
        save_new_photo(message, app)
    elif command in get_command('save_new_video'):
        save_new_video(message, app)
    elif command in get_command('save_new_voice_message'):
        save_new_voice_message(message, app)
    elif command in get_command('search'):
        search(message)
    elif command in get_command('send_saved_message'):
        send_saved_message(message, msg)
    elif command in get_command('send_saved_photo'):
        send_saved_photo(message, app)
    elif command in get_command('send_saved_video'):
        send_saved_video(message, app)
    elif command in get_command('send_saved_voice_message'):
        send_saved_voice_message(message, app)
    elif command in get_command('spam'):
        spam(message, app, msg)
    elif command in get_command('time'):
        time(message)
    elif command in get_command('trust'):
        trust_user(message, msg, client, app)
    elif command in get_command('write'):
        write(message)
        

@app.on_message()
def main(client, message):
    blacklist(message, app)
    trust(message, app)

    # delete this
    my_func(message, config, app)


if __name__ == "__main__":
    print("Hello! Started working...")
    app.run()
    print("GoodBye!")