import validators
from urllib.parse import urlparse


def is_valid_url(url):
    valid_length = len(url) <= 255
    valid_struct = validators.url(url)
    return valid_length and valid_struct


def normalize_url(url):
    normalized_url = urlparse(url)
    scheme = normalized_url.scheme
    hostname = normalized_url.hostname
    return f"{scheme}://{hostname}"
