import re
from pathlib import Path

if __name__ == "__main__":
    from encode import encode
else:
    from src.encode import encode

def dynamic_text(root, key, value):
    """ Creates a text html module from type layers in photoshop using
        font_type, font_size, font_tracking, font_color
        The text is spaced with smartobjects laballed SPACER_X
        X = The height of the spacer
    """
    resources = Path(root).joinpath("resources")
    text_template = Path(resources).joinpath("TEXT_TEMPLATE.htm")
    with open(f"{text_template}", "r") as f:
        template = f.read()

    html_list = []

    for n, layer in enumerate(value):
        if isinstance(layer, list):
            if "Header".lower() in layer[0].lower():
                name = "Header"
            elif "Paragraph".lower() in layer[0].lower():
                name = "Paragraph"
            else:
                name = layer

            font_size = layer[2]
            mobile_font_size = mobile_font_class(font_size)
            padding_top = calc_padding_top(font_size)
            font_type = encode(layer[1])
            font_tracking = layer[3]
            font_color = layer[4]

            if "Paragraph" in name:
                line_height = calc_line_height(font_size)
            else:
                line_height = font_size
            try:
                with open(Path(resources).joinpath(f"{name}.htm"), "r") as module_html:
                    data = module_html.read()
                    data = data.replace("{{ mobile_font_size }}", str(mobile_font_size))
                    data = data.replace("{{ padding_top }}", str(padding_top))
                    data = data.replace("{{ font_type }}", str(font_type))
                    data = data.replace("{{ font_size }}", str(font_size))
                    data = data.replace("{{ line_height }}", str(line_height))
                    data = data.replace("{{ font_tracking }}", str(font_tracking))
                    data = data.replace("{{ font_color }}", str(font_color))
                    html_list.append(data)
            except FileNotFoundError as e:
                print(e)

        elif isinstance(layer, str) and 'spacer'.lower() in layer.lower():
            height = spacer_height(layer)
            try:
                if n is not 0 and n is not len(value)-1:
                    height = height_calc_rendered(height, value[n-1], value[n+1])
            except KeyError as e:
                print(e)
            
            try:
                with open(Path(resources).joinpath(f"SPACER.htm"), "r") as module_html:
                    data = module_html.read()
                    data = data.replace("{{ height }}", str(height))
                    data = data.replace("{{ padding }}", str(int(height) - 1))
                    html_list.append(data)
            except FileNotFoundError as e:
                print(e)
        
    html = template.replace("{{ content }}", "\n".join(html_list))
    return html

def spacer_height(layer):
    return re.findall(r'_(\d+)', layer)[0]

def calc_padding_top(font_size):
    return round((10 * font_size) / 100)

def calc_line_height(font_size):
    if font_size <=18:
        height = round((150 * font_size) / 100)
        return height
    return font_size

def mobile_font_class(font_size):
    if font_size >= 40:
        return 'header_xl'
    elif font_size > 30 and font_size <= 35:
        return 'header_l'
    elif font_size > 25 and font_size <= 30:
        return 'header_m'
    elif font_size > 20 and font_size <= 25:
        return 'header_sm'
    elif font_size <= 20:
        return 'header_s'
    return None

def height_calc_rendered(height, a, b):
    font_a = a[2]
    font_b = b[2]

    rendered = (font_a * 0.62)
    spacing_diff_a = (font_a - rendered) / 2

    rendered = (font_b * 0.62)
    spacing_diff_b = (font_b - rendered) / 2

    height = int(height) - (round(spacing_diff_a) + round(spacing_diff_b))
    if height < 0:
        height = 0

    return height
