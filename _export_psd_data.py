import os
from pathlib import Path
from pprint import pprint
import json

from psd_tools import PSDImage

from src.dynamic_text import dynamic_text
from src.psdtools import (
    artboard_layers, 
    module_groups, 
    mobile_artboard,
    extract_psd_module_text,
    extract_psd_module_button
)
from src.helpers import (
    psd_filename,
    convert_digit_length,
    json_dump
)
from config import MODULE_DATA

root = os.path.dirname(__file__)


def collate_data(modules, user_directory):
    """ Collate data from the into dict/json and export
    """
    count = 0
    image_count = 0

    data = dict()
    for module in modules:
        name = []

        data[count] = dict()

        # Module
        data[count]["Module"] = module.name

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
            
        count += 1

    json_dump(Path(user_directory).joinpath(MODULE_DATA), data, 'w')


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

    collate_data(modules, user_directory)