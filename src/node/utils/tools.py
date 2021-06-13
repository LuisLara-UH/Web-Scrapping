def find_separator(text: str):
    index = 0
    while len(text) > index and not text[index] == '%':
        index += 1

    if len(text) == index:
        return None
    return index