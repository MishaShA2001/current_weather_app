"""Criterions to check numbers"""


def check_for_positive_int(text: str) -> bool:
    """Checks if a text can be interpreted as a positive int

    :param text: string to check
    :return: True if it's a positive int, False otherwise
    """
    try:
        if int(text) > 0:
            return True
        return False
    except ValueError:
        return False
