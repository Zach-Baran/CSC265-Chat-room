from django.utils.crypto import get_random_string


def create_token():
    token = get_random_string(length=6)
    return token
