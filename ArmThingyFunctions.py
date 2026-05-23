import re
from datetime import timedelta


def flatten(json_dict):
    """
    Flatten a nested JSON dictionary into a single-level dictionary.

    :param json_dict: Nested JSON dictionary to be flattened
    :return: Flat dictionary
    """
    flattened_dict = {}
    for key, value in json_dict.items():
        if isinstance(value, dict):
            flattened_dict.update(flatten(value))
        else:
            flattened_dict[key] = value
    return flattened_dict


def pretty_time_delta(td: timedelta) -> str:
    """
    Generate a string representation of a timedelta object in a human-readable format.
    Example:
        td = timedelta(days=2, hours=3, minutes=45, seconds=15)
        pretty_time_delta(td) -> "2d 3h 45m 15s"
    :param td: timedelta object
    :return: Human-readable string representation of the timedelta
    """
    output_str = ""
    if td.days > 0:
        output_str += f"{td.days}d "
    if td.seconds >= 3600:
        output_str += f"{td.seconds // 3600}h "
    if td.seconds % 3600 >= 60:
        output_str += f"{(td.seconds % 3600) // 60}m "
    output_str += f"{td.seconds % 60}s"
    return output_str


def snake_case_to_human_case(snake_case_str):
    """
    Convert snake_case string to human-readable format.
    Example:
        snake_case_to_human_case('snake_case_string') -> 'Snake Case String'
    :param snake_case_str: Snake case string to be converted
    :return: Human-readable string
    """
    output_words = []
    words = snake_case_str.split('_')
    for word in words:
        # Words that are fully uppercase
        if word in ("id",):
            output_words.append(word.upper())
        # Words to capitalize first letter only
        else:
            output_words.append(word.capitalize())
    return ' '.join(output_words)


def camel_case_to_snake_case(string: str) -> str:
    """
    Convert camelCase string to snake_case.
    Example:
        camel_case_to_snake_case('camelCaseString') -> 'camel_case_string'
    :param string: Camel case string to be converted
    :return: Snake case string
    """
    # Match an uppercase letter that follows a lowercase letter/digit and separate with underscore
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    # Match multiple consecutive uppercase letters followed by a lowercase letter and separate with underscore
    s2 = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return s2.lower()
