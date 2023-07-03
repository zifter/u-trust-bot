from external.tg.callback_data import CallbackData


def test_save_and_load_ok():
    callback = CallbackData('test me', {'value': 1, "param": 'user answer'})
    result = CallbackData.deserialize(callback.serialize())

    assert callback == result
