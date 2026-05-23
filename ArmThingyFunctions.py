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
    underscore_separation = r'\1_\2'
    # Separate lowercase from uppercase
    s1 = re.sub('([a-z])([A-Z])', underscore_separation, string)
    # Separate uppercase acronyms from following words
    s2 = re.sub('([A-Z]+)([A-Z][a-z])', underscore_separation, s1)
    # Separate letters from digits
    s3 = re.sub(r'([a-zA-Z])(\d)', underscore_separation, s2)
    # Separate digits from letters
    s4 = re.sub(r'(\d)([a-zA-Z])', underscore_separation, s3)
    return s4.lower()
