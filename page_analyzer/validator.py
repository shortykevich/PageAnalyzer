import re


def is_valid_url(url):
    valid_length = len(url) <= 255
    valid_struct = re.match(
        '^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$', url)  # noqa:W605
    return valid_length and valid_struct
