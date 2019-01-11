from psd_tools import PSDImage
import os
import json
from pathlib import Path
from bs4 import BeautifulSoup, Tag

""" Export image from a photoshop file """
psd = 'test.psd'
psd_load = PSDImage.load(Path(os.path.dirname(__file__)) / psd)

module_list_from_psd = []
BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'
encoding_dict = {
    'Ä': '&Auml;', 'ä': '&auml;', 'É': '&Eacute;',
    'é': '&eacute;', 'Ö': '&Ouml;', 'ö': '&ouml;',
    'Ü': '&Uuml;', 'ü': '&uuml;', 'ß': '&szlig;',
    '‘': '&lsquo;', '’': '&rsquo;', '“': '&ldquo;',
    '”': '&rdquo;', '€': '&euro;', '£': '&pound;',
    '…': '...', u'\xa0': '&nbsp;'
}


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
                    # font_type = layer.text.rstrip().replace('\r', '<br class="d_h" /> ')
                    font_type = layer.text.rstrip().replace('\r', ' ')

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

    except AttributeError:
        pass


def get_module_html(name):
    file = open('modules.json')
    data = json.load(file)
    for key, value in data.items():
        if name == key:
            return value


def encode(a):
    """
        Iterate through each character in a string and replace with encoded version from encoding_dict
    """
    b = []
    if isinstance(a, list):
        for item in a:
            a = [str(char).replace(char, encoding_dict.get(char, char)) for char in item]
            a = "".join(a)
            b.append(a)
    elif isinstance(a, str):
        a = [str(char).replace(char, encoding_dict.get(char, char)) for char in a]
        a = "".join(a)
        b.append(a)

    return b


def no_blank(a):
    """
        Adds &nbsp; before the last word of each text string to prevent single words on one line
    """
    b = a.rsplit(' ', 1)
    try:
        if b[1]:
            b[1] = f'&nbsp;{b[1]}'
            b = ''.join(b)
    except:
        if b:
            b = ''.join(b)
    return b

def replace(name):
    html = get_module_html(name[0])
    soup = BeautifulSoup(html, 'html.parser')

    module_text = []
    for a in soup.findAll('a'):
        if not a.find('img'):
            module_text.append(a.text)
    go = 0
    encode_module_text = encode(module_text)

    if len(encode_module_text) == len(name) - 1:
        for mod in encode_module_text:
            go += 1
            a = encode(name[go][0])
            no_blank(a[0])
            html = html.replace(mod, a[0], 1)
    else:
        print(f'{{}}ALERT! {name[0]} module has not been updated.{{}} There are {len(encode_module_text)} html and {len(name) - 1} psd text containers.\n'.format(RED, END))

    return html


def write_out(html_list):
    data = html_list
    counter = 4
    with open('modules.htm', 'w') as f:
        for v in data:
            counter += 1

            """ Save image if counter length is less than 9 """
            if counter <= 9:
                # f.write(f'\t\t\t<div data-content-region-name="region_0{counter}">\n')
                f.write(v)
                # f.write('\n\t\t\t</div>')
                f.write('\n\n')

            """ Save image if counter length is greater than 9 """
            if counter > 9:
                # f.write(f'\t\t\t<div data-content-region-name="region_{counter}">\n')
                f.write(v)
                # f.write('\n\t\t\t</div>')
                f.write('\n\n')

    f.close()


print(f'The file {{}}{psd}{{}} is being parsed.\n'.format(BLUE, END))

for i in psd_load.layers:
    if 'MOBILE'.lower() in i.name.lower():
        """ Get module names from psd """
        modules = get_module_names_content(i)

        html_list = []
        """ Get module html from modules.json """
        for mod in modules:
            print(f'{{}}{mod[0]}{{}}'.format(BLUE, END))
            """ replace text in html """
            try:
                html_list.append(replace(mod))
            except TypeError:
                pass

            """ write out to file """
            write_out(html_list=html_list)
