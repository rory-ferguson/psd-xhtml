import os
from pathlib import Path

from psd_tools import PSDImage
from bs4 import BeautifulSoup

from src.encode import encode
from src.dynamic_text import dynamic_text
from src.psdtools import list_of_psd_layers, list_of_modules, get_mobile_artboard
from src.helpers import (
    psd_filename,
    convert_to_m,
    write_to_file,
    get_module_html_from_json,
    parse_module_text,
    add_nbsp_to_last_word,
    write_modules_list
)

root = os.path.dirname(__file__)


def replace_text_in_html(key, value):
    """
        Replaces the text in the html modules with the text from the
        PSD, only if the amout of text containers match.
        ie
        BUTTON_01 has one text container and BUTTON_02 has two text containers
    """
    html = get_module_html_from_json(root, key)
    soup = BeautifulSoup(html, "html.parser")

    html_module_text = parse_module_text(soup)

    count = 0
    if len(html_module_text) == len(value):
        for html_text in html_module_text:
            psd_module_text = encode(value[count][1])
            psd_module_text = add_nbsp_to_last_word(psd_module_text)
            html = html.replace(html_text, psd_module_text, 1)
            count += 1
    else:
        print(
            f"ALERT! {key} module has not been updated."
            f"There are {len(html_module_text)} html and {len(value)} psd text containers.\n"
        )
    return html


def replace_module_with_html(modules):
    lst = []
    for i in modules:
        name = i[0]
        value = i[1]
        if isinstance(i, tuple) and "DYNAMIC_TEXT".lower() in name.lower():
            lst.append(dynamic_text(root, name, value))
        elif isinstance(i, tuple) and len(value) > 0:
            if 'button'.lower() in name.lower() and '_D'.lower() in name.lower() :
                name = convert_to_m(name)
            try:
                lst.append(replace_text_in_html(name, value))
            except TypeError as e:
                print(f"{name} not included.")
                lst.append("")
                continue
        else:
            lst.append(get_module_html_from_json(root, name))
        print(name)
    return lst


if __name__ == "__main__":
    user_directory = input('PSD path:')

    psd = psd_filename(
        user_directory, message="PSD name (can be blank or without file extension):"
    )

    print(f"\nLoading {psd}")
    psd_load = PSDImage.open(Path(user_directory).joinpath(psd))
    print(f"Finished loading {psd}\n")
    print(f"The file {psd} is being parsed.\n")

    artboard = get_mobile_artboard(psd_load)

    layers = list_of_psd_layers(artboard)

    if artboard:
        modules = list_of_modules(layers)

    html_data = replace_module_with_html(modules)

    write_to_file(path=user_directory, data=html_data)
    write_modules_list(path=user_directory, modules=modules)
