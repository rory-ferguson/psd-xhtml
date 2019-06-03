from psd_tools import PSDImage
import os
import json
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from colorama import Fore, Style

module_list_from_psd = []

root = os.path.dirname(__file__)

user_directory = input('PSD path:')

psd = input('PSD name:')

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

print(f'\nLoading {Fore.BLUE}{psd}{Style.RESET_ALL}')
psd_load = PSDImage.open(path_of_psd)
print(f'Finished loading {Fore.BLUE}{psd}{Style.RESET_ALL}\n')


def get_module_names_content(container):
    try:
        for layer in reversed(list(container)):
            if layer.is_visible() and layer.kind == 'group':
                """ Module list names """
                """ ['TEXT_02'] """
                name = [layer.name]
                module_list_from_psd.append(name)
                """ Module contents"""
                """ ['TEXT_02', ['HEADER THREE', 'FuturaPT-Demi', '20px', '#1a1a1a', '0.08em']] """
                recurse(layer, m=name)

        return module_list_from_psd

    except AttributeError:
        pass


def recurse(container, m):
    """ Recursive loop over each layer to extract all the text
    """
    try:
        for layer in reversed(list(container.descendants())):
            if layer.is_visible():
                if layer.kind == 'type':
                    """ font_type """
                    font_type = layer.text.rstrip().replace('\r', ' ')

                    lst = [font_type]
                    m.append(lst)

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


def no_blank(a):
    """ this feature needs work and is not active
        Adds &nbsp; before the last word of each text string to prevent single words on one line
    """
    try:
        b = a.rsplit(' ', 1)

        if b[1]:
            b[1] = f'&nbsp;{b[1]}'
            b = ''.join(b)

        if not b[1]:
            b = ''.join(b)

    except IndexError:
        pass

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
            """ this feature needs work and is not active
            no_blank(a[0])
            """
            html = html.replace(m, a[0], 1)
    else:
        print(f'{Fore.RED}ALERT! {name[0]} module has not been updated.{Style.RESET_ALL} '
              f'There are {len(encode_module_text)} html and {len(name) - 1} psd text containers.\n')

    return html


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

for i in psd_load:
    if 'MOBILE'.lower() in i.name.lower():
        mobileArtboard = i
        """ Get module names from psd """
        modules = get_module_names_content(i)
        html_lst = []
        """ Get module html from modules.json """
        for mod in modules:
            print(f'{Fore.BLUE}{mod[0]}{Style.RESET_ALL}'.format(BLUE, END))
            """ replace text in html """
            try:
                html_lst.append(replace(mod))
            except TypeError:
                pass


            """ write out to file """
            write_out(lst=html_lst)


if mobileArtboard is None:
    print('There was a problem.')
    print('Please ensure the artboard names include one of the below')
    print('_Desktop or _Mobile')
    sys.exit()
