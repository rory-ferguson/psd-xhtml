
def colour_to_hex(colour):
    """ Convert floating point colour to hex
    """
    t = []
    if isinstance(colour, list):
        for index, item in enumerate(colour[1:4]):
            t.append((int(round(item * 255))))
        return '#%02x%02x%02x' % (t[0], t[1], t[2])
