def decor(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Sorry, try again"

    return wrapper


contacts = {}


@decor
def add(*args):
    name = args[0]
    phone_number = args[1]
    contacts[name] = phone_number
    return f"This is ADD, name {name}, phone {phone_number}"


def hello(*args):
    return "How can I help you?"


def change(*args):
    name = args[0]
    phone_number = args[1]
    if name in contacts.keys():
        contacts[name] = phone_number
        return f"This is CHANGE, phone {phone_number} for name {name}"
    else:
        return f"This name {name} is not found. Please input correct name"


def phone(*args):
    name = args[0]
    if name in contacts.keys():
        return f"This is phone {contacts[name]} for name {name}"
    else:
        return f"This name {name} is not found. Please input correct name"


def show_all(*args):
    return f"The contacts are {contacts}"


def close(*args):
    print("Good Bye!")
    exit(0)




COMMANDS = {
    "add": add,
    "hello": hello,
    "change": change,
    "phone": phone,
    "show_all": show_all,
    "close": close,
    "good_bye": close,
    "exit": close,
}


def command_parser(user_input: str):
    chunks = user_input.strip().split(" ")
    command_name = chunks[0].lower()
    args = chunks[1:]

    if command_name in COMMANDS.keys():
        return COMMANDS[command_name], args
    else:
        return None, None


def main():
    while True:
        user_input = input(">>> ")
        if user_input == ".":
            break
        command, data = command_parser(user_input)

        if not command:
            print("Sorry, unknown command")
        else:
            print(command(*data))


if __name__ == "__main__":
    main()
