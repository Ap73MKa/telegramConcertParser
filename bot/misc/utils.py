from re import sub


def simplify_string(name: str) -> str:
    return sub('[^a-zA-Zа-яА-Я]', '', name.lower().strip().replace('ё', 'е'))
