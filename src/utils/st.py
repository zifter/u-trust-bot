import random
import string
from typing import Optional


def rand_string_id(total_length: Optional[int] = None, rand_length: int = 10,
                   prefix: str = '', suffix: str = '', is_lowercase: bool = True):

    if total_length is not None:
        rand_length = total_length - len(prefix) - len(suffix)

    if rand_length is None or rand_length <= 0:
        raise ValueError(f'wrong args: {total_length} {rand_length}, {prefix}, {suffix}')

    if is_lowercase:
        root = ''.join(random.choice(string.ascii_lowercase) for i in range(rand_length))
    else:
        root = ''.join(random.choice(string.ascii_uppercase) for i in range(rand_length))
    return f'{prefix}{root}{suffix}'
