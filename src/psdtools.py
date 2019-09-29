import sys

from psd_tools.constants import Tag

from src.helpers import (
    floating_point_to_hex, 
    rgb_to_hex, 
    clean_name,
    convert_to_m
)
from src.encode import encode


def artboard_layers(artboard):
    lst = []
    for layer in reversed(list(artboard)):
        if (
            layer.is_visible()
            and layer.kind == "group"
            and "header".lower() not in layer.name.lower()
        ):
            lst.append(layer)
    return lst

def module_names(layers):
    """ Return a list of the modules names
        ['1COL_B_Swap_850_M']
    """
    lst = []
    for module in reversed(list(layers)):
        print(module)
        if module.is_visible() and module.kind == "group":
            lst.append(module.name)
    return lst

def module_names_validated(json, layers):
    """ Return a list of the modules names, validated by modules.json
        ['1COL_B_Swap_850_M']
    """
    lst = []
    for module in reversed(list(layers)):
        if module.is_visible() and module.kind == "group":
            name = module.name
            name = clean_name(name.strip())
            if 'button'.lower() in name.lower():
                name = convert_to_m(name)
            print(name)
            if name in json:
                """
                remove ' copy' etc
                replace _D > _M
                """
                lst.append(name)
    return lst

def module_groups(layers: list) -> list:
    """ Return a list of each modules Group information
        [Group('1COL_B_Swap_850_M' size=850x285)]
    """
    lst = []
    for module in layers:
        if module.is_visible() and module.kind == "group":
            try:
                lst.append(module)
            except KeyError as e:
                pass
    return lst

def mobile_artboard(psd_load):
    for artboard in psd_load:
        if "MOBILE".lower() in artboard.name.lower() and artboard.kind == "artboard":
            return artboard
    if not artboard:
        print(f"There was a problem.")
        print(f'Please ensure the artboard name includes "mobile"')
        sys.exit()


def desktop_artboard(psd_load):
    for artboard in psd_load:
        if "DESKTOP".lower() in artboard.name.lower() and artboard.kind == "artboard":
            return artboard
    if not artboard:
        print(f"There was a problem.")
        print(f'Please ensure the artboard name includes "desktop"')
        sys.exit()

def extract_psd_module_text(module):
    lst = []
    try:
        for layer in reversed(list(module.descendants())):
            if (
                layer.is_visible()
                and layer.kind == "smartobject"
                and "spacer".lower() in layer.name.lower()
            ):
                lst.append(layer.name)

            elif layer.is_visible() and layer.kind == "type":
                """ font_type """
                style_sheet = layer.engine_dict["StyleRun"]["RunArray"][0]
                font_type = layer.text.rstrip().replace("\r", " ")
                font_size = int(
                    round(style_sheet["StyleSheet"]["StyleSheetData"]["FontSize"] / 2)
                )
                font_tracking = f"{style_sheet['StyleSheet']['StyleSheetData']['Tracking'] / 1000:.2f}"

                font_color = style_sheet["StyleSheet"]["StyleSheetData"]["FillColor"][
                    "Values"
                ]
                font_color = floating_point_to_hex(list(font_color))
                font_styles = dict()
                font_styles['Name'] = layer.name
                font_styles['Type'] = font_type
                font_styles['Font_Size'] = font_size
                font_styles['Letter-Spacing'] = font_tracking
                font_styles['Font-Colour'] = font_color
                lst.append(font_styles)

    except AttributeError:
        pass

    return lst

def extract_psd_module_button(module):
    lst = []
    try:
        for layer in reversed(list(module.descendants())):
            if (
                layer.is_visible()
                and layer.kind == "shape"
                and layer.name == "Rectangle"
            ):
                button_styles = dict()
                try:
                    shapelayer_data = layer.tagged_blocks.get_data(Tag.SOLID_COLOR_SHEET_SETTING)._items[b'Clr ']

                    color_array = []
                    for k, v in shapelayer_data.items():
                        color_array.append(round(int(v)))
                    button_styles['Background_Color'] = rgb_to_hex(tuple(color_array))
                except AttributeError as e:
                    button_styles['Background_Color'] = None

                if layer.has_stroke():
                    button_styles['Stroke'] = True
                else:
                    button_styles['Stroke'] = False
                
                lst.append(button_styles)

    except AttributeError as e:
        pass

    return lst