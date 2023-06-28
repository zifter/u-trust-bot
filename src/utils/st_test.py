import pytest

from utils.st import rand_string_id, format_duration


def test_rand_string_id():
    length = 10
    prefix = 'pf_'
    suffix = '_sf'
    v = rand_string_id(total_length=length, prefix=prefix, suffix=suffix)

    assert len(v) == 10
    assert v.startswith(prefix)
    assert v.endswith(suffix)


@pytest.mark.parametrize("seconds, expected_output", [
    (123456789, "1428 days, 21 hours, 33 minutes, 9 seconds"),
    (30, "30 seconds"),
    (3600, "1 hour"),
    (7200, "2 hours"),
    (86400, "1 day"),
    (0, "0 seconds"),
    (-1234, "undefined"),
    (9999999999, "115740 days, 17 hours, 46 minutes, 39 seconds"),
    (3661, "1 hour, 1 minute, 1 second"),
    (61, "1 minute, 1 second"),
])
def test_format_time(seconds, expected_output):
    assert format_duration(seconds) == expected_output
