from configparser import ConfigParser
from json import loads
from os import listdir


def config():
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    return config


def get_saved_messages(message):
    read = open(f'{config()["DATA"]["path"]}/message.txt', 'r',
                    encoding='UTF-8', errors='replace')
    lines = read.readlines()
    read.close()

    result = ''
    for line in lines:
        result += f'`{loads(line)["name"]}`\n'
    message.edit(f"💾 **Your messages:**\n{result}")


def get_saved_photos(message):
    result = ''
    for i in listdir(f'{config()["DATA"]["path"]}/photo'):
        result += f'`{i[:-4]}`\n'
    message.edit(f"📷 **Your photos:**\n{result}")


def get_saved_videos(message):
    result = ''
    for i in listdir(f'{config()["DATA"]["path"]}/video'):
        result += f'`{i[:-4]}`\n'
    message.edit(f"📹 **Your videos:**\n{result}")


def get_saved_voice_messages(message):
    result = ''
    for i in listdir(f'{config()["DATA"]["path"]}/voice'):
        result += f'`{i[:-4]}`\n'
    message.edit(f"🎙 **Your voice messages:**\n{result}")