from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__private_value = None
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, value):
        self.__private_value = value




class Name(Field):
    pass


class Phone(Field):
    pass


class Birthday(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday

    def add_phone(self, add_phone: Phone):
        self.phones.append(add_phone)

    def remove_phone(self, removable_phone: Phone):
        self.phones = self.phones.remove(removable_phone)

    def change_phone(self, changeable_phone: Phone, new_phone: Phone):

        for i, n in enumerate(self.phones):
            if n == changeable_phone:
                self.phones[i] = new_phone

        return self.phones

    def days_to_birthday(self, birthday, now):

        date_birthday = datetime.strptime(birthday, '%m-%d-%Y').date()
        delta1 = datetime(now.year, date_birthday.month, date_birthday.day)
        delta2 = datetime(now.year + 1, date_birthday.month, date_birthday.day)
        if delta1 > now:
            return (delta1 - now).days
        else:
            return (delta2 - now).days

    def __str__(self):
        return self.name.value + repr(self.phones) + repr(self.birthday)

    def __repr__(self):
        return str(self)


class AddressBook(UserDict[str, Record]):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def change_record(self, record: Record):
        if record.name.value in self.data:
            self.data[record.name.value] = record
        else:
            raise Exception(f"This name {record.name.value} is not found. Please input correct name")


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
    name = args[0]
    phone_number = args[1]
    if len(args) == 3:
        birthday = args[2]
        contacts.add_record(
            Record(
                Name(name),
                Phone(phone_number),
                Birthday(birthday)
            )
        )
    elif len(args) == 2:
        contacts.add_record(
            Record(
                Name(name),
                Phone(phone_number),
            )
        )
    return f"This is ADD, name {name}, phone {phone_number}"


@input_error
def add_phone(*args):
    name = args[0]
    phone_number = args[1]
    if name in contacts.keys():
        contacts[name].add_phone(Phone(phone_number))
        return f"This is ADD, name {name}, phone {phone_number}"
    else:
        return f"This Name {name} is not found in contacts"


@input_error
def remove_phone(*args):
    name = args[0]
    phone_number = args[1]
    if name in contacts.keys():
        if Phone(phone_number) in contacts[name].phones:
            contacts[name].remove_phone(Phone(phone_number))
            return f"This is REMOVE phone {phone_number} from name {name}"
        else:
            return f"This {phone_number} is not defined"
    else:
        return f"This Name {name} is not found in contacts"


@input_error
def change_phone(*args):
    name = args[0]
    phone_number = args[1]
    new_phone_number = args[2]
    if name in contacts.keys():
        if Phone(phone_number) in contacts[name].phones:
            contacts[name].change_phone(Phone(phone_number), Phone(new_phone_number))
            return f"This is CHANGE phone {phone_number} to new number {new_phone_number} for name {name}"
        else:
            return f"This phone number {phone_number} is not defined"
    else:
        return f"This Name {name} is not found in contacts"


def hello(*args):
    return "How can I help you?"


@input_error
def change(*args):
    name = args[0]
    phone_number = args[1]
    if name in contacts.keys():
        contacts.change_record(
            Record(
                Name(name),
                [Phone(phone_number)]
            )
        )
        return f"This is CHANGE, phone {phone_number} for name {name}"
    else:
        raise Exception("Name is not found in contacts")


@input_error
def phone(*args):
    name = args[0]
    if name in contacts.keys():
        return f"This is phone {contacts.get(name).phones} for name {name}"

    else:
        raise Exception("Name is not found in contacts")


@input_error
def days_to_birthday(*args):
    name = args[0]
    phone = args[1]
    birthday = args[2]
    if name in contacts.keys():
        return f"This is phone {contacts.get(name).phones} for name {name}"

    else:
        raise Exception("Name is not found in contacts")



def show_all(*args):
    pattern = '{0:10} {1:10} {2:10}\n'
    table = pattern.format("Name", "Phones", "Birthday")
    for record in contacts.values():
        table += pattern.format(
            record.name.value,
            ", ".join(map(repr, record.phones)),
            record.birthday.value
        )
    return table


def close(*args):
    print("Good Bye!")
    exit(0)


COMMANDS = {
    "add": add,
    "phone add": add_phone,
    "phone change": change_phone,
    "phone remove": remove_phone,
    "hello": hello,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "close": close,
    "good bye": close,
    "exit": close,
}


def command_parser(user_input: str):
    for key_word, command in COMMANDS.items():
        if user_input.lower().startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")
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
