from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


    def change_record(self, record):
        if record.name.value in self.data:
            self.data[record.name.value] = record
        else:
            raise Exception(f"This name {record.name.value} is not found. Please input correct name")

    def get_record(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
            raise Exception(f"This name {name} is not found. Please input correct name")


class Record:
    def __init__(self, name, phone):
        self.name = name
        self.phones = [phone]

    def __str__(self):
        return self.name.value + repr(self.phones)

    def __repr__(self):
        return str(self)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


    def __repr__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    pass


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Sorry, reading from invalid index"
        except Exception as e:
            return str(e)

    return wrapper


contacts = AddressBook()


@input_error
def add(*args):
    try:
        name = args[0]
        phone_number = args[1]
    except IndexError:
        raise Exception("Please, input name and phone")
    contacts.add_record(
        Record(
            Name(name),
            [Phone(phone_number)]
        )
    )
    return f"This is ADD, name {name}, phone {phone_number}"


def hello(*args):
    return "How can I help you?"


@input_error
def change(*args):
    try:
        name = args[0]
        phone_number = args[1]
    except IndexError:
        raise Exception("Please, input name and phone")

    contacts.change_record(
        Record(
            Name(name),
            [Phone(phone_number)]
        )
    )

    return f"This is CHANGE, phone {phone_number} for name {name}"



@input_error
def phone(*args):
    try:
        name = args[0]

        raise Exception("Please specify name")
    return f"This is phone {contacts.get_record(name).phones} for name {name}"



def show_all(*args):
    pattern = '{0:10}  {1}\n'
    table = pattern.format("Name", "Phones")
    for record in contacts.values():

        table += pattern.format(record.name.value, ", ".join(map(repr, record.phones)))
    return table


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


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'

    print('All Ok)')

    main()
