import os


def sort_with_rows(file: str) -> int:
    with open(os.path.join(_dir, file), 'r', encoding='utf-8') as input_file:
        return input_file.read().count('\n')

_dir = 'files'
my_files = os.listdir(_dir)
my_files.sort(key=sort_with_rows)

with open('sorted_file', 'w', encoding='utf-8') as output_file:
    for file_ in my_files:
        with open(os.path.join(_dir, file_), 'r', encoding='utf-8') as input_file:
            f = input_file.read()
            print(file_, f.count('\n')+1, f, sep='\n', file=output_file)
