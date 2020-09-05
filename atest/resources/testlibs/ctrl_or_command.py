import platform


def ctrl_or_command_key():
    if platform.system() == "Darwin":
        return "COMMAND"
    return "CONTROL"
