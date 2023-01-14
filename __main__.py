from pyrogram import Client, filters
from configparser import ConfigParser
from ast import literal_eval
from commands import *

config = ConfigParser()
config.read('config.ini', encoding="utf-8")
api_id = int(config['API']['api_id'])
api_hash = config['API']['api_hash']
print("api_id =", api_id)
print("api_hash =", api_hash)

app = Client("my_account", api_id=api_id, api_hash=api_hash)


@app.on_message(filters.me)
def main(client, message):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
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
    elif len(msg) < 2: return
    else: return

    command = msg[0]
    if command in get_command('all_id'):
        all_id(message)
    elif command in get_command('blacklist'):
        blacklist()


if __name__ == "__main__":
    print("Hello! Started working...")
    app.run()
    print("GoodBye!")