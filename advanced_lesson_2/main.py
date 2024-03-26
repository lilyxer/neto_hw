import csv

from csv_core import load_csv, write_lo_file
from row_core import get_row, parce_row


LOAD_LINK = 'https://raw.githubusercontent.com/netology-code/py-homeworks-advanced/master/5.Regexp/phonebook_raw.csv'
RAW_FILE = 'raw.csv'
HEADERS = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
_TMP: dict = {}
OUTPUT = 'output.csv'


if __name__ == '__main__' and load_csv(link=LOAD_LINK, file_name=RAW_FILE):
    with open(OUTPUT, 'w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()

    my_gen = get_row(RAW_FILE)
    while my_gen:
        try:
            row = parce_row(next(my_gen))
            if all(map(row.get, HEADERS)):
                write_lo_file(file_name=OUTPUT, stroke=row, fields=HEADERS)
            else:
                name = f"{row['lastname']}{row['firstname']}"
                if name in _TMP:
                    row = {k: v for k, v in row.items() if v}
                    _TMP[name].update(row)
                else:
                    _TMP[name] = row
        except StopIteration:
            break
    if _TMP:
        for value in _TMP.values():
            write_lo_file(file_name=OUTPUT, stroke=value, fields=HEADERS)