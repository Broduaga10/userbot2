import os.path
import shutil
from configparser import ConfigParser

from pyrogram.raw.functions.contacts import ResolveUsername


def blacklist(message, msg, client, app):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    dtext = config['DATA']['path']
    name = 