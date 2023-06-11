from utils.st import rand_string_id


def test_rand_string_id():
    length = 10
    prefix = 'pf_'
    suffix = '_sf'
    v = rand_string_id(total_length=length, prefix=prefix, suffix=suffix)

    assert len(v) == 10
    assert v.startswith(prefix)
    assert v.endswith(suffix)
