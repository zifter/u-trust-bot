from utrust.commander import Commander, Section, Command

test_layout = [
    Section('First', [
        Command('start', 'enter smth', None),
        Command('auth', 'auth me', None),
    ]),
    Section('Second', [
        Command('delme', 'delme it', None),
        Command('giveme', 'giveme it', None),
    ])
]


def test_commander_get_start_description():
    cmder = Commander(test_layout, 'Hello World!')

    got = cmder.start_description()
    expected = "Hello World!\n\nYou can control me by sending these commands:\n\n<b>First</b>\n/start enter smth\n/auth auth me\n\n<b>Second</b>\n/delme delme it\n/giveme giveme it"

    assert got == expected
