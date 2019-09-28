import os
import json
import re
from pathlib import Path


def floating_point_to_hex(colour):
    """ Convert floating point colour to hex
    """
    t = []
    if isinstance(colour, list):
        for index, item in enumerate(colour[1:4]):
            t.append((int(round(item * 255))))
        return "#%02x%02x%02x" % (t[0], t[1], t[2])

def rgb_to_hex(colour):
    """ Convert rgb colour to hex
    """
    return "#%02x%02x%02x" % tuple(colour)

def psd_filename(path: str, message: str):
    user_input = input(f"{message}\n")
    if user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if user_input in file:
                    return file

    if not user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if ".psb" in file or ".psd" in file:
                    return file


def directory_exists(path: str) -> bool:
    if os.path.exists(os.path.dirname(path)):
        return True
    return False


def get_module_html_from_json(root, name):
    """ Get html matching json key with name
    """
    name = clean_name(name.strip())
    try:
        f = open(Path(root).joinpath("modules.json"))
    except FileNotFoundError:
        sys.exit("modules.json is missing from the repository, check the README")
    data = json.load(f)
    for key, value in data.items():
        if name.strip() == key.strip():
            return value


def clean_name(name):
    return re.split(' ', name)[0]


def convert_to_m(name):
    return re.split('(_D)', name)[0] + '_M'


def write_to_file(path, data):
    """ Write out html to file
    """
    counter = 4
    with open(Path(path).joinpath("modules.htm"), "w") as f:
        for v in data:
            if isinstance(v, str):
                counter += 1
                if counter <= 9:
                    f.write(
                        f'\t\t\t<div data-content-region-name="region_0{counter}">\n'
                    )
                    f.write(v)
                    f.write("\n\t\t\t</div>")
                    f.write("\n\n")

                if counter > 9:
                    f.write(
                        f'\t\t\t<div data-content-region-name="region_{counter}">\n'
                    )
                    f.write(v)
                    f.write("\n\t\t\t</div>")
                    f.write("\n\n")
            else:
                print(type(v))
    f.close()

def write_modules_list(path, modules):
    with open(Path(path).joinpath("modules.txt"), "w") as file:
        file.writelines(i[0] + '\n' for i in modules)
        file.close()

def parse_module_text(soup):
    lst = []
    for a in soup.findAll("a"):
        if not a.find("img"):
            lst.append(a.text)
    return lst


def add_nbsp_to_last_word(word):
    word = word.rsplit(' ', 1)
    if len(word) > 1:
        word[1] = f'&nbsp;{word[1]}'
        return ''.join(word)
    else:
        return ''.join(word)


def convert_digit_length(count):
    if isinstance(count, int):
        if count <= 9:
            return f"0{count}"
        else:
            return f"{count}"