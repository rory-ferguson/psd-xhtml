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
                module_list_from_psd.append(layer.name)

    except AttributeError as Argument:
        print(f'{Argument}')


for i in psd_load.layers:
    if 'MOBILE'.lower() in i.name.lower():
        get_modules(i)


file = open('modules.json')
data = json.load(file)
counter = 4

with open('modules.htm', 'w') as f:

    for i in module_list_from_psd:
        counter += 1
        for k, v in data.items():
            if i == k:
                f.write(f'\t\t\t<div data-content-region-name="region_0{counter}">\n')
                f.write(v)
                f.write('\n\t\t\t</div>\n\n')

f.close()
