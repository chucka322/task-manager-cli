def parse_message(message):

    parts = message.strip().split(maxsplit=1)

    command = parts[0]

    if len(parts) > 1:
        argument = parts[1]
    else:
        argument = ""

    return command, argument
