import sys 
sys.path.append("..")

import pytest 

from . import filetype, process
from setup.logger import *

Log = get_logger('ERROR')

def test_sp():
    cmd = 'ls'
    cmd_output = process.sp(Log, cmd)
    assert cmd_output != 0

def test_invalid_file_extension():
    supported_types = ['tgd', 'YY_', 'T00', 'T02']
    invalid_extensions = ['txt', '1234', 'a']
    for extension in invalid_extensions:
        
        with pytest.raises(SystemExit) as e:
            filetype(Log,f'infile.{extension}', supported_types)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 9
