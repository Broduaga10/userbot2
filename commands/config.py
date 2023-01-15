from configparser import ConfigParser


def cfg(message, msg):
    config = ConfigParser()
    config.read('config.ini', encoding="utf-8")
    try:
        command = msg[1].lower()
    except:
        text = f'<pre>🛠 Config:</pre>\n' \
                f"**Prefix:**  {config['PREFIXES']['prefix']}\n" \
                f"**Prefix Delete:**  {config['PREFIXES']['delete_prefix']}\n" \
                f"**Delete text:**  {config['DATA']['delete_text']}\n" \
                f'\n<pre>📝 Commands:</pre>\n'
        for command in config['COMMANDS']:
            text += f"**{command}**:  {config['COMMANDS'][command]}\n"
        message.edit(text)
        return

    if command in ['prefix', 'префикс']:
        sections = 'PREFIXES'
        option = 'prefix'
    elif command in ['delprefix', 'делпрефикс']:
        sections = 'PREFIXES'
        option = 'delete_prefix'
    elif command in ['deltext', 'dtext', 'делтекст', 'дтекст']:
        sections = 'DATA'
        option = 'delete_text'
    else:
        message.edit('⚠️ **Unknown command** ⚠️\n\n**Choose one of these:**\n["prefix", "префикс"] \n' \
                     '["delprefix", "делпрефикс"]\n["deltext", "dtext", "делтекст", "дтекст"]')
        return

    new_text = str(msg[2:]).replace("'", '"')
    message.edit(f'✅ **Done!**\nNew {option}: {new_text}')
    config.set(sections, option, new_text)
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)