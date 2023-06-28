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


def format_duration(seconds):
    if seconds < 0:
        return 'undefined'

    if seconds == 0:
        return '0 seconds'

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    time_parts = []
    if days > 0:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        time_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    return ', '.join(time_parts)
