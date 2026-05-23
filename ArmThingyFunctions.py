import re
from datetime import timedelta


def flatten(json_dict):
    flattened_dict = {}
    for key, value in json_dict.items():
        if isinstance(value, dict):
            flattened_dict.update(flatten(value))
        else:
            flattened_dict[key] = value
    return flattened_dict


def pretty_time_delta(td: timedelta):
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
    # Match an uppercase letter that follows a lowercase letter/digit and separate with underscore
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string)
    # Match multiple consecutive uppercase letters followed by a lowercase letter and separate with underscore
    s2 = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return s2.lower()
