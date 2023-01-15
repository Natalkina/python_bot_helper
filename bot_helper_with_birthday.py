from collections import UserDict
from datetime import date, datetime


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
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if value.isnumeric():
            self._value = value
        else:
            raise Exception("Please enter correct phone number")


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        if datetime.strptime(value, "%Y-%m-%d"):
            self._value = date.fromisoformat(value)
        else:
            raise Exception("Please enter date number as 'YYYY-MM-DD'")

    def days_diff(self, date):

        delta1 = datetime(date.year, self.value.month, self.value.day)
        delta2 = datetime(date.year + 1, self.value.month, self.value.day)
        if delta1 > date:
            return (delta1 - date).days
        else:
            return (delta2 - date).days

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone]
        self.birthday = birthday

    def add_phone(self, add_phone: Phone):
        self.phones.append(add_phone)

    def remove_phone(self, removable_phone: Phone):
        self.phones = [n for n in self.phones if n != removable_phone]

    def change_phone(self, changeable_phone: Phone, new_phone: Phone):

        for i, n in enumerate(self.phones):
            if n == changeable_phone:
                self.phones[i] = new_phone

        return self.phones



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

    def iterator(self, page_size: int) -> list[Record]:
        page = [None] * page_size
        idx = 0
        for record in self.data.values():
            page[idx] = record
            idx += 1
            if idx == page_size:
                yield page
                idx = 0
        yield page[:idx]



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

    birthday = Birthday(args[2]) if len(args) == 3 else None

    contacts.add_record(
        Record(
            Name(name),
            Phone(phone_number),
            birthday
        )
    )

    message = f"This is ADD, name {name}, phone {phone_number}"
    if birthday:
        message += f", and birthday {birthday.value}"

    return message


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
    if name in contacts.keys():
        record = contacts[name]
        if record.birthday:
            days = record.birthday.days_diff(datetime.now())

            return f"The {days} days left to birthday of contact {name}"

        else:
            raise Exception(f"This contact {name} has no information about birthday")
    else:
        raise Exception("Please input correct name")



def show_all(*args):
    pattern = '{0:10} {1:10} {2:10}\n'
    table = pattern.format("Name", "Phones", "Birthday")

    for page in contacts.iterator(5):
        for record in page:
            table += pattern.format(
                record.name.value,
                ", ".join(map(repr, record.phones)),
                str(record.birthday.value) if record.birthday else "None"
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
    "days to birthday": days_to_birthday,
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
    main()
