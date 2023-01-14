from configparser import ConfigParser
from json import loads


def delete_message(message):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    path = config['DATA']['path']

    name = ' '.join(message.text.split()[2:])
    
    read = open(f'{path}/message.txt', 'r',
                    encoding='UTF-8', errors='replace')
    lines = read.readlines()
    read.close()

    print("name - "+name)
    x = True
    result = ""
    for line in lines:
        dictionary = loads(line)
        if dictionary["name"] == name:
            x = False
            continue
        print(dictionary["name"])
        result += line
    if x:
        message.edit(f"**No such text in file**")
        return

    write = open(f'{path}/message.txt', 'w',
                    encoding='UTF-8', errors='replace')
    write.write(result)
    write.close()
    message.edit(f"**Done!**\nText has been removed")