
def encode(a):
    """ Encodes each character in a string
        :param: a
        :ptype: str or list
        :return: b
        :rtype: list
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