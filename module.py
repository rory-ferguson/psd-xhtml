from psd_tools import PSDImage
import os
import json
from pathlib import Path
from collections import namedtuple
from bs4 import BeautifulSoup, Tag
import re
from html.parser import HTMLParser

""" Export image from a photoshop file """
psd = 'test.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)

module_list_from_psd  = []


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
                    # font_type = layer.text.rstrip().replace('\r', '\n').rstrip()
                    font_type = layer.text.rstrip().replace('\r', '<br class="d_d_b" />')

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
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for a in soup.findAll('a'):
        if not a.find('img'):
            tags.append(a.text)
    go = 0

    encoding_dict = {
        'Ä': '&Auml;', 'ä': '&auml;', 'É': '&Eacute;',
        'é': '&eacute;', 'Ö': '&Ouml;', 'ö': '&ouml;',
        'Ü': '&Uuml;', 'ü': '&uuml;', 'ß': '&szlig;',
        '‘': '&lsquo;', '’': '&rsquo;', '“': '&ldquo;',
        '”': '&rdquo;', '€': '&euro;', '£': '&pound;',
        '…': '...'
    }

    encoded_tags = []
    for i in tags:
        a = [str(char).replace(char, encoding_dict.get(char, char)) for char in i]
        a = "".join(a)
        encoded_tags.append(a)
    print(encoded_tags)

    if len(encoded_tags) == len(name) - 1:
        for i in encoded_tags:
            go += 1
            # print(i, name[go][0])
            html = html.replace(i, name[go][0])
    # print(html)

    return html


def write_out(html_list):
    data = html_list
    counter = 4
    with open('modules.htm', 'w') as f:
        for v in data:
            counter += 1
            f.write(f'\t\t\t<div data-content-region-name="region_0{counter}">\n')
            f.write(v)
            f.write('\n\t\t\t</div>\n\n')

    f.close()


for i in psd_load.layers:
    if 'MOBILE'.lower() in i.name.lower():
        """ Get module names from psd """
        modules = get_module_names_content(i)

        html_list = []
        """ Get module html from modules.json """
        for mod in modules:
            """ replace text in html """
            html_list.append(replace(mod))
            """ write out to file """
            write_out(html_list=html_list)
