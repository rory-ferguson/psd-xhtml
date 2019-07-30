import os
import json
import sys
from pathlib import Path

from psd_tools import PSDImage
from bs4 import BeautifulSoup

from src.colour_to_hex import colour_to_hex
from src.encode import encode

root = os.path.dirname(__file__)


def extract_module_text(module):
    lst = []
    try:
        for layer in reversed(list(module)):
            if (
                layer.is_visible() 
                and layer.kind == 'smartobject' 
                and 'spacer'.lower() in layer.name.lower()
            ):
                lst.append(layer.name)

            elif layer.is_visible() and layer.kind == 'type':
                """ font_type """
                style_sheet = layer.engine_dict['StyleRun']['RunArray'][0]
                font_type = layer.text.rstrip().replace('\r', ' ')
                font_size = int(round(style_sheet['StyleSheet']['StyleSheetData']['FontSize'] / 2))
                font_tracking = f"{style_sheet['StyleSheet']['StyleSheetData']['Tracking'] / 1000:.2f}"

                font_color = style_sheet['StyleSheet']['StyleSheetData']['FillColor']['Values']
                font_color = colour_to_hex(list(font_color))
                type_array = [layer.name, font_type, font_size, font_tracking, font_color]
                lst.append(type_array)

    except AttributeError:
        pass

    return lst

def get_module_html(name):
    """ Get html matching json key with name
    """
    try:
        f = open(Path(root).joinpath('modules.json'))
    except FileNotFoundError:
        sys.exit('modules.json is missing from the repository, check the README')
    data = json.load(f)
    for key, value in data.items():
        if name.strip() == key.strip():
            return value

def replace(key, value):
    html = get_module_html(key)
    soup = BeautifulSoup(html, 'html.parser')
    html_module_text = []
    for a in soup.findAll('a'):
        if not a.find('img'):
            html_module_text.append(a.text)

    count = 0
    if len(html_module_text) == len(value):
        for m in html_module_text:
            b = encode(value[count][1])
            html = html.replace(m, b[0], 1)
            count += 1
    else:
        print(f'ALERT! {key} module has not been updated. '
              f'There are {len(html_module_text)} html and {len(value)} psd text containers.\n')
    return html

def dynamic_text(key, value):
    """ Creates a text module from type layer in photoshop using
        font_type, font_size, font_tracking, font_color
        :param: key, value
        :ptype: str, list
        :return: html
        :rtype: str
    """
    resources = Path(root).joinpath('resources')
    text_template = Path(resources).joinpath('TEXT_TEMPLATE.htm')
    with open(f'{text_template}', 'r') as f:
        template = f.read()
    lst = []
    for layer in value:
        if isinstance(layer, list):
            if 'Header'.lower() in layer[0].lower():
                name = 'Header'
            elif 'Paragraph'.lower() in layer[0].lower():
                name = 'Paragraph'
            else:
                name = name
            try:
                with open(Path(resources).joinpath(f'{name}.htm'), 'r') as module_html:
                    data = module_html.read()
                    font_type = encode(layer[1])[0]
                    data = data.replace('{{ font_type }}', str(font_type))
                    data = data.replace('{{ font_size }}', str(layer[2]))
                    data = data.replace('{{ line_height }}', str(layer[2]))
                    data = data.replace('{{ font_tracking }}', str(layer[3]))
                    data = data.replace('{{ font_color }}', str(layer[4]))
                    lst.append(data)
            except FileNotFoundError as e:
                print(e)

        elif isinstance(layer, str):
            height = layer.split('_')[1]
            try:
                with open(Path(resources).joinpath(f'SPACER.htm'), 'r') as module_html:
                    data = module_html.read()
                    data = data.replace('{{ height }}', str(height))
                    data = data.replace('{{ padding }}', str(int(height) - 1))
                    lst.append(data)
            except FileNotFoundError as e:
                print(e)

    html = template.replace('{{ content }}', '\n'.join(lst))
    return html

def write_out(data):
    """ Write out html to file
        :param: data
        :ptype: list
    """
    counter = 4
    with open(Path(user_directory).joinpath('modules.htm'), 'w') as f:
        for v in data:
            counter += 1

            """ Save image if counter length is less than 9 """
            if counter <= 9:
                f.write(f'\t\t\t<div data-content-region-name="region_0{counter}">\n')
                f.write(v)
                f.write('\n\t\t\t</div>')
                f.write('\n\n')

            """ Save image if counter length is greater than 9 """
            if counter > 9:
                f.write(f'\t\t\t<div data-content-region-name="region_{counter}">\n')
                f.write(v)
                f.write('\n\t\t\t</div>')
                f.write('\n\n')

    f.close()

def get_artboard():
    for artboard in psd_load:
        if 'MOBILE'.lower() in artboard.name.lower() and artboard.kind == 'artboard':
            return artboard

        else:
            print(f'There was a problem.')
            print(f'Please ensure the artboard name includes "mobile"')
            sys.exit()

def layer_list(artboard):
    lst = []
    for layer in reversed(list(artboard)):
        if (
            layer.is_visible() 
            and layer.kind == 'group'
        ):
            lst.append(layer)
    return lst

def main(modules):
    lst = []
    for module in modules:
        if module.is_visible() and module.kind == 'group':
            lst.append((module.name, extract_module_text(module)))
        else:
            lst.append(module.name)
    return lst


if __name__ == "__main__":
    # user_directory = input('PSD path:')
    user_directory = 'C:\\Users\\rory.ferguson\\Documents\\test\\email_module'
    # psd = input('PSD name:')
    psd = 'text.psd'
    path_of_psd = Path(user_directory).joinpath(psd)
    # print(f'\nLoading {psd}')
    psd_load = PSDImage.open(path_of_psd)
    # print(f'Finished loading {psd}\n')
    # print(f'The file {psd} is being parsed.\n')

    artboard = get_artboard()
    layers = layer_list(artboard)
    
    if artboard:
        modules = main(layers)

    html_data = []
    for i in modules:
        name = i[0]
        value = i[1]
        if isinstance(i, tuple) and 'DYNAMIC_TEXT'.lower() in name.lower():
            html_data.append(dynamic_text(name, value))
        elif isinstance(i, tuple) and len(value) > 0:
            html_data.append(replace(name, value))
        else:
            html_data.append(get_module_html(name))

    write_out(data=html_data)
