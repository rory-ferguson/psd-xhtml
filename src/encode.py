def encode(word):
    """ Encodes each character in a string
        :param: a
        :ptype: str
        :rtype: str
    """
    encoding_dict = {
        "Ä": "&Auml;",
        "ä": "&auml;",
        "É": "&Eacute;",
        "é": "&eacute;",
        "Ö": "&Ouml;",
        "ö": "&ouml;",
        "Ü": "&Uuml;",
        "ü": "&uuml;",
        "ß": "&szlig;",
        "‘": "&lsquo;",
        "’": "&rsquo;",
        "“": "&ldquo;",
        "”": "&rdquo;",
        "€": "&euro;",
        "£": "&pound;",
        "…": "...",
        u"\xa0": "&nbsp;",
        "–": "&ndash;",
    }
    encoded_word = []
    if isinstance(word, str):
        word = [str(char).replace(char, encoding_dict.get(char, char)) for char in word]
        word = "".join(word)
        encoded_word.append(word)
    return ''.join(encoded_word)

if __name__ == "__main__":
    print(encode('Phasellus eget abc tgd.'))