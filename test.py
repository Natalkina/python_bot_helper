import csv


def read_from_csv():
    with open('addressbook.csv', newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            yield row

for row in read_from_csv():
    print(row)
