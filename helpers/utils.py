import string
import random


def generate_random_name(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choices(chars, k=size))
