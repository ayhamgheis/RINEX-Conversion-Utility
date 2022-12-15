from . import settings

def test_temp_folder():
    test_input = settings.get_temp_folder("user input dir",'default dir')
    assert test_input == 'user input dir'

def test_no_log():
    no_log = settings.set_logger(None, None)
    assert no_log == 'INFO'

def test_user_log():
    for level in ['WARNING','INFO','DEBUG', 'ERROR']:
        user_log = settings.set_logger(level, None)
        assert user_log == level

def test_invalid_cfg():
    user_specified_path = '/invalid/path/to/config.cfg'
    default = 'config.cfg'
    config = settings.get_cfg(user_specified_path, default)
    assert config == default


