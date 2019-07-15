from psd_tools import PSDImage
import os
import json
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from colorama import Fore, Style

root = os.path.dirname(__file__)

# user_directory = input('PSD path:')
user_directory = 'X:\\WebDesign\\AW19\\emails\\z_approved\\test'

# psd = input('PSD name:')
psd = 'text.psd'

if psd:
    for file in os.listdir(user_directory):
        if psd in file:
            psd = file
            path_of_psd = Path(user_directory).joinpath(file)
            break

if not psd:
    for file in os.listdir(user_directory):
        if '.psb' in file or '.psd' in file:
            psd = file
            path_of_psd = Path(user_directory).joinpath(file)
            break

if not path_of_psd:
    path_of_psd = Path(user_directory).joinpath(psd)

# print(f'\nLoading {Fore.BLUE}{psd}{Style.RESET_ALL}')
psd_load = PSDImage.open(path_of_psd)
# print(f'Finished loading {Fore.BLUE}{psd}{Style.RESET_ALL}\n')


def module_list(layer):
    """ Return module list from the psd file with text
        :param: layer
        :ptype: psd_tools.api.layers.Group
        :return: modules
        :rtype: list
    """
    try:
        if layer.is_visible() and layer.kind == 'group':
            """ Module list names """
            name = [layer.name]
            modules.append(name)
            extract_module_text(layer, module=name)

        return modules

    except AttributeError:
        pass

def colour_to_hex(font_color):
    t = []
    for index, item in enumerate(font_color[1:4]):
        t.append((int(round(item * 255))))
    return '#%02x%02x%02x' % (t[0], t[1], t[2])

def extract_module_text(container, module):
    """ Extract the module text from the psd file
        example: ['TEXT_02', ['HEADER THREE', 'FuturaPT-Demi', '20px', '#1a1a1a', '0.08em']]
        :param: container, module
        :ptype: psd_tools.api.layers.Group, list
        :return: module
        :rtype: list
    """
    try:
        for layer in reversed(list(container.descendants())):
            if layer.is_visible() and layer.kind == 'type':
                """ font_type """
                style_sheet = layer.engine_dict['StyleRun']['RunArray'][0]

                font_type = layer.text.rstrip().replace('\r', ' ')
                font_size = int(round(style_sheet['StyleSheet']['StyleSheetData']['FontSize'] / 2))
                font_tracking = f"{style_sheet['StyleSheet']['StyleSheetData']['Tracking'] / 1000:.2f}em"  # font-tracking
                font_color = style_sheet['StyleSheet']['StyleSheetData']['FillColor']['Values']  # font-colour
                font_color = colour_to_hex(font_color)  # convert colour to hex code
                type_data = [font_type], [layer.name], [font_size]
                module.append(type_data)
        return module

    except AttributeError:
        pass


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


def encode(a):
    """ Iterate through each character in a string and replace with encoded version from encoding_dict
    """
    encoding_dict = {
        'Ä': '&Auml;', 'ä': '&auml;', 'É': '&Eacute;',
        'é': '&eacute;', 'Ö': '&Ouml;', 'ö': '&ouml;',
        'Ü': '&Uuml;', 'ü': '&uuml;', 'ß': '&szlig;',
        '‘': '&lsquo;', '’': '&rsquo;', '“': '&ldquo;',
        '”': '&rdquo;', '€': '&euro;', '£': '&pound;',
        '…': '...', u'\xa0': '&nbsp;', '–': '&ndash;'
    }
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
        for m in encode_module_text:
            go += 1
            a = encode(name[go][0])
            html = html.replace(m, a[0], 1)
    else:
        print(f'{Fore.RED}ALERT! {name[0]} module has not been updated.{Style.RESET_ALL} '
              f'There are {len(encode_module_text)} html and {len(name) - 1} psd text containers.\n')

    return html


def some_func(module):
    resources = Path(root) / 'resources'
    text_template = Path(resources) / 'TEXT_TEMPLATE.htm'
    with open(f'{text_template}') as f:
        template = f.read()
    name = module[1][1][0]
    font_text = module[1][0][0]
    font_size = module[1][2][0]


def write_out(lst):
    data = lst
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

print(f'The file {Fore.BLUE}{psd}{Style.RESET_ALL} is being parsed.\n')

for artboard in psd_load:
    if 'MOBILE'.lower() in artboard.name.lower() and artboard.kind == 'artboard':
        mobile_artboard = artboard
        modules = []

        for layer in reversed(list(artboard)):
            modules = module_list(layer)
        print(modules)

        """ Get module html from modules.json """
        html_lst = []
        for mod in modules:
            # print(f'{Fore.BLUE}{mod[0]}{Style.RESET_ALL}')

            if mod[0] == 'DYNAMIC_TEXT':
                some_func(mod)
                pass
            else:
                """ replace text in html """
                try:
                    html_lst.append(replace(mod))
                except TypeError:
                    pass

            """ write out to file """
            write_out(lst=html_lst)


# if mobile_artboard is None:
#     print('There was a problem.')
#     print('Please ensure the artboard names include one of the below')
#     print('_Desktop or _Mobile')
#     sys.exit()
