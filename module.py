from psd_tools import PSDImage
import os
import json
from pathlib import Path

""" Export image from a photoshop file """
psd = 'test.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)

module_list_from_psd = []


def get_modules(container):
    try:
        for layer in container.layers:
            if layer.visible and layer.kind == 'group':
                print(layer.name)
                module_list_from_psd.append(layer.name)
                recurse(layer, name=layer.name)

    except AttributeError as Argument:
        print(f'{Argument}')


def recurse(container, name):
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
                    font_color = style_sheet[b'StyleSheet'][b'StyleSheetData'][b'FillColor'][b'Values']

                    """ Font Color > Hex Code """
                    tuple_list = []
                    for index, item in enumerate(font_color[1:4]):
                        tuple_list.append((int(round(item * 255))))
                    font_color = '#%02x%02x%02x' % (tuple_list[0], tuple_list[1], tuple_list[2])

                    print(font_type, font_family, font_size, font_color, font_tracking)

                recurse(layer, name=name)

    except AttributeError as Attribute:
        # print(f'{Attribute}')
        pass


for i in psd_load.layers:
    if 'MOBILE'.lower() in i.name.lower():
        get_modules(i)
