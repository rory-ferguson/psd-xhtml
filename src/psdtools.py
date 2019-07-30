import sys

from src.helpers import colour_to_hex
from src.encode import encode

def list_of_psd_layers(artboard):
    lst = []
    for layer in reversed(list(artboard)):
        if (
            layer.is_visible()
            and layer.kind == "group"
            and "header".lower() not in layer.name.lower()
        ):
            lst.append(layer)
    return lst


def list_of_modules(modules):
    lst = []
    for module in modules:
        if module.is_visible() and module.kind == "group":
            try:
                lst.append((module.name, extract_psd_module_text(module)))
            except KeyError as e:
                pass
        else:
            lst.append(module.name)
    return lst


def get_mobile_artboard(psd_load):
    for artboard in psd_load:
        if "MOBILE".lower() in artboard.name.lower() and artboard.kind == "artboard":
            return artboard
    if not artboard:
        print(f"There was a problem.")
        print(f'Please ensure the artboard name includes "mobile"')
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
                font_color = colour_to_hex(list(font_color))
                type_array = [
                    layer.name,
                    font_type,
                    font_size,
                    font_tracking,
                    font_color,
                ]
                lst.append(type_array)

    except AttributeError:
        pass

    return lst
