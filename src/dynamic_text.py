from pathlib import Path

if __name__ == "__main__":
    from encode import encode
else:
    from src.encode import encode

def dynamic_text(root, key, value):
    """ Creates a text module from type layer in photoshop using
        font_type, font_size, font_tracking, font_color
    """
    resources = Path(root).joinpath("resources")
    text_template = Path(resources).joinpath("TEXT_TEMPLATE.htm")
    with open(f"{text_template}", "r") as f:
        template = f.read()
    lst = []
    for layer in value:
        if isinstance(layer, list):
            if "Header".lower() in layer[0].lower():
                name = "Header"
            elif "Paragraph".lower() in layer[0].lower():
                name = "Paragraph"
            else:
                name = name
            try:
                with open(Path(resources).joinpath(f"{name}.htm"), "r") as module_html:
                    data = module_html.read()

                    font_type = encode(layer[1])
                    data = data.replace("{{ font_type }}", str(font_type))
                    data = data.replace("{{ font_size }}", str(layer[2]))
                    data = data.replace("{{ line_height }}", str(layer[2]))
                    data = data.replace("{{ font_tracking }}", str(layer[3]))
                    data = data.replace("{{ font_color }}", str(layer[4]))
                    lst.append(data)
            except FileNotFoundError as e:
                print(e)

        elif isinstance(layer, str):
            height = layer.split("_")[1]
            try:
                with open(Path(resources).joinpath(f"SPACER.htm"), "r") as module_html:
                    data = module_html.read()
                    data = data.replace("{{ height }}", str(height))
                    data = data.replace("{{ padding }}", str(int(height) - 1))
                    lst.append(data)
            except FileNotFoundError as e:
                print(e)

    html = template.replace("{{ content }}", "\n".join(lst))
    return html
