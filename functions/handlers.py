def unchaining(string: str) -> str:
    """
    remove brackets in tags
    """
    string = string[string.find('>') + 1:]
    string = string[:string.find('<')]
    return ' '.join(string.split())
