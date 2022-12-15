import os
from pathlib import Path
''' For removing the folder housing the RINEX 2.11 observation files '''

def temp_folder(Log, temp_folder, working):
    ''' Deletes the folder at temp_folder '''
    p = Path(f'{working}/{temp_folder}')
    Log('I', f'Deleting {working}/{temp_folder}')
    [Path.unlink(x) for x in p.iterdir()] # removes Files from inside temp folder
    p.rmdir() # removes temp folder
