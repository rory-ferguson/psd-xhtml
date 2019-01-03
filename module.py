from psd_tools import PSDImage
import os
import json
from pathlib import Path
from collections import namedtuple
from bs4 import BeautifulSoup
import re

""" Export image from a photoshop file """
psd = 'test.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)

module_list_from_psd = []


def get_module_names_content(container):
    try:
        for layer in container.layers:
            if layer.visible and layer.kind == 'group':
                """ Module list names """
                """ ['TEXT_02'] """
                name = [layer.name]
                module_list_from_psd.append(name)

                """ Module contents"""
                """ ['TEXT_02', ['HEADER THREE', 'FuturaPT-Demi', '20px', '#1a1a1a', '0.08em']] """
                recurse(layer, name=layer.name, module=name)

        return module_list_from_psd

    except AttributeError as Argument:
        # print(f'{Argument}')
        pass


def recurse(container, name, module):
    """
        Recursive loop over each layer to extract all the text
    """
    try:
        for layer in container.layers:
            if layer.visible:
                if layer.kind == 'type':

                    """ font_type """
                    font_type = layer.text.rstrip().replace('\r', '\n')

                    """ font_type using EngineData """
                    # print(str(layer.engine_data[b'EngineDict'][b'Editor'][b'Text']).rstrip().replace('\r', '\n'))

                    """ EngineData """
                    # print(layer.engine_data[b'EngineDict'])

                    """ Font Size """
                    style_sheet = layer.engine_data[b'EngineDict'][b'StyleRun'][b'RunArray'][0]
                    font_size = f"{round(style_sheet[b'StyleSheet'][b'StyleSheetData'][b'FontSize'] / 2)}px"

                    """ Font Family """
                    font_family = layer.fontset[0][b'Name']

                    """ Font tracking """
                    font_tracking = f"{style_sheet[b'StyleSheet'][b'StyleSheetData'][b'Tracking'] / 1000:.2f}em"

                    """ Font Color """
                    font_colour = style_sheet[b'StyleSheet'][b'StyleSheetData'][b'FillColor'][b'Values']

                    """ Font Color > Hex Code """
                    tuple_list = []
                    for index, item in enumerate(font_colour[1:4]):
                        tuple_list.append((int(round(item * 255))))
                    font_colour = '#%02x%02x%02x' % (tuple_list[0], tuple_list[1], tuple_list[2])

                    lst = [font_type, font_family, font_size, font_colour, font_tracking]
                    module.append(lst)

                recurse(layer, name=name, module=module)

    except AttributeError as Attribute:
        # print(f'{Attribute}')
        pass


def get_module_html(name):
    file = open('modules.json')
    data = json.load(file)

    for key, value in data.items():
        if name == key:
            return value


def replace(name):
    html = get_module_html(name[0])
    font_type = name[1][0]
    soup = BeautifulSoup(html, 'html.parser')
    emails = soup.find_all('td')
    print(emails)


for i in psd_load.layers:
    if 'MOBILE'.lower() in i.name.lower():
        """ Get module names from psd """
        modules = get_module_names_content(i)
        # for i in modules:
        #     print(i[0])

        """ Get module html from modules.json """
        for mod in modules:
            # get_module_html(mod[0])
            # print(get_module_html(mod[0]))
            """ replace """
            replace(mod)
