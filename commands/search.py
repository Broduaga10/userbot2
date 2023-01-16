from os import listdir
from configparser import ConfigParser


def search(message):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    path = config['DATA']['path']
    name = ' '.join(message.text.split()[2:])

    all_listdir = [listdir(f'{path}/photo'), listdir(f'{path}/video'), listdir(f'{path}/voice')]
    path_names = ["**🖼 Photo:**\n", "**📽 Video:**\n", "**🔊 Voice:**\n"]

    r = [None, list(name)]
    result = ''
    for j in range(len(all_listdir)):

        res = ''
        for el in all_listdir[j]:
            r[0] = ''.join(el[:-4])
            if r[0].find(name) > -1:
                res += '- `' + el[:-4] + '`\n'
        if res:
            result += '\n' + path_names[j] + res

    if result:
        message.edit(result)
    else:
        message.edit('🔍 __Not found__')
    