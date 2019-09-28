import os
from pathlib import Path
from pprint import pprint
import json

from psd_tools import PSDImage
from bs4 import BeautifulSoup

from src.encode import encode
from src.dynamic_text import dynamic_text
from src.psdtools import (
    artboard_layers, 
    module_groups, 
    mobile_artboard, 
    module_names,
    extract_psd_module_text,
    extract_psd_module_button
)
from src.helpers import (
    psd_filename,
    convert_to_m,
    write_to_file,
    get_module_html_from_json,
    parse_module_text,
    add_nbsp_to_last_word,
    write_modules_list,
    convert_digit_length
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

def collate_data(modules):
    """ Collate data from the into dict/json and export
    """
    count = 0
    image_count = 0

    data = dict()
    for module in modules:
        count += 1
        name = []

        data[count] = dict()

        # Module_Name
        data[count]["Module_Name"] = module.name

        # Images
        if module.kind == "group" and module.visible:
            for layer in reversed(list(module)):
                if (
                    "image".lower() in layer.name.lower()
                    and layer.kind == "group"
                    and layer.visible
                ):
                    image_count += 1
                    
                    name.append(convert_digit_length(image_count))
                    data[count]["Images"] = name

        # Font Styles
        text_styles = extract_psd_module_text(module)
        if text_styles:
            data[count]["Text_Styles"] = text_styles

        # Button Styles
        button_styles = extract_psd_module_button(module)
        if button_styles:
            data[count]["Button_Styles"] = button_styles

    with open('module_data.json', 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    # user_directory = input('PSD path:')
    user_directory = 'C:\\Users\\Rory.Ferguson\\test'

    psd_name = psd_filename(
        user_directory, message="PSD name (can be blank or without file extension):"
    )

    print(f"\nLoading {psd_name}")
    psd = PSDImage.open(Path(user_directory).joinpath(psd_name))
    print(f"Finished loading {psd_name}\n")
    print(f"The file {psd_name} is being parsed.\n")

    artboard = mobile_artboard(psd)

    layers = artboard_layers(artboard)

    modules = module_groups(layers)

    collate_data(modules)

    # html_data = replace_module_with_html(modules)
    
    # write_to_file(path=user_directory, data=html_data)
    # write_modules_list(path=user_directory, modules=modules)
