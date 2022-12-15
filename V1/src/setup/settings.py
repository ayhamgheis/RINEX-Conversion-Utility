import configparser
import argparse
import sys, os

def argparse_setup(parser):
    ''' sets up the different command line arguments '''

    parser.add_argument(
        '-in',
        help='Name of input file',
        action='store',
        required=True
    )
    parser.add_argument(
        '-cfg',
        help='Path to cfg file',
        action='store'
    )
    parser.add_argument(
        '-logging',
        help='Set logging level. Determines Verbosness of output',
        choices=['WARNING','INFO','DEBUG', 'ERROR']
    )
    parser.add_argument(
        '-qc',
        help='use -qc to pass output through quality check program',
        action='store_true'
    )
    parser.add_argument(
        '-systems',
        help='List the single letter identifiers for the systems you wish to '
            'extract (g,r,s,e,c)'
    )
    parser.add_argument(
        '-working_dir',
        help='The directory on the system you want to use for information '
            'handling'
    )
    parser.add_argument(
        '-temp_folder',
        help='Rinex 2.11 observation files will be created into this folder. '
            'It will be placed inside the working Directory (default $PWD '
            'unless changed in config file.'
    )
    parser.add_argument(
        '-output',
        help='Name the output file. Will generate RINEX 3.04 name if discluded'
    )
    parser.add_argument(
        '-station',
        help='Manually set the name of the reciever station',
        action='store'  
    ) 
    return parser

def get_working_dir(arg_working_dir: str, parse_working_dir: str) -> str:
    ''' sets the working directory depending on arguments or config
    
        details on its purpose is in the readme
        Args:
            arg_working_dir
                if the -working_dir flag is used, it will be set to this
            parse_working_Dir
                if the -working_dir flag is not used, it will use the value
                in the config file.
        Returns:
            string representing the directory to be used.
        '''
    if arg_working_dir == '.' or parse_working_dir == '.':
        print(f'Do not use \'.\' in a directory. Using $PWD instead')
        return(os.getenv('PWD'))
    if arg_working_dir != None:
        if arg_working_dir[0] == '$':
            return os.getenv(arg_working_dir[1:])
        return arg_working_dir   
    else:
        if parse_working_dir[0] == '$':
            return os.getenv(parse_working_dir[1:])
        return  parse_working_dir

def get_temp_folder(arg_temp_folder,  parse_temp_folder):
    ''' sets the temp directory depending on arguments or config
    
        details on its purpose is in the readme
        Args:
            arg_temp_dir
                if the -temp_dir flag is used, it will be set to this
            parse_working_Dir
                if the -temp_dir flag is not used, it will use the value
                in the config file.
        Returns:
            string representing the temp directory to be used.
        '''
    if arg_temp_folder != None:
        return arg_temp_folder
    else:
        return parse_temp_folder    

    
def get_display_order(parse_cfg : str, systems: list) -> dict:
    ''' creates a dictionary representing how the data output should be structured 
    
        Args:
            parse_cfg
                Information from the config file containing constellations 
                and their signals
            systems
                list of systems that we want reported. Observations will be output
                in the same order as this list
        Returns:
            display_order
                list of key value pairs
                key "sv_systems"
                    The satellite systems that we want printed
                key g,e,c,r
                    the signals associated with these signals
    '''
    display_order = dict()
    systems = [x.lower() for x in systems]
    for x in parse_cfg:
        display_order[x] = parse_cfg[x].split(',')
    display_order["sv_systems"] = systems
    return display_order

def input_file(arg_in : str) -> str:
    ''' Gets the name of the input file from command line arguments '''
    if arg_in is None:
        raise ValueError
    return arg_in

def set_logger(arg_log : str, parse_log : str) -> str:
    ''' sets the logging level '''
    default = 'INFO' 
    if arg_log is not None and arg_log in ['WARNING','INFO','DEBUG', 'ERROR']:
        return arg_log
    elif parse_log is not None:
        return parse_log
    else:
        return default

def set_systems(arg_sys : str, parse_sys : str) -> list:
    ''' Sets the list of GNSS systems we wish to extract '''
    default = ['G','R','S','E','C']
    systems = list()
    if arg_sys is not None:
        if ',' in arg_sys:
            arg_sys_L = arg_sys.split(',')
            for sys in arg_sys_L:
                if sys.upper() in default and sys.upper() not in systems:
                    systems.append(sys.upper())
            return systems
        elif arg_sys.upper() in default:
            systems.append(arg_sys.upper())
            return systems
        else:
            raise argparse.ArgumentTypeError
    elif parse_sys is not None:
        if ',' in parse_sys:
            parse_sys_L = parse_sys.split(',')
            for sys in parse_sys_L:
                if sys.upper() in default and sys.upper() not in systems:
                    systems.append(sys.upper())
            return systems
        elif parse_sys.upper() in default:
            systems.append(parse_sys.upper())
        else:
            raise configparser.ParsingError
    else:
        return default

def get_supported_types(supported):
    ''' Gets a list of the supported file types '''
    extensions = [x for x in supported]
   # print('extensions', extensions)
    supported_types = dict()
    for x in extensions:
        supported_types[x] = supported[x]
    supported_types['T00'] = 'TRIMBLE'
    supported_types['T02'] = 'TRIMBLE' 
    #print('supported',supported_types)
    return supported_types

def get_output_name(arg_op: str, parse_op: str):
    ''' sets the output name for the output file 
    
        If no output name is given, it will generate a proper
        RINEX 3.04 name'''
    if arg_op is not None:
        return arg_op
    else:
        return None

def get_cfg(cfg_name,cfg_file):
    ''' Determines if a config file exists or not 

        if the file does not exist, it checks for the default file
        in the current folder.
    '''
    try:
        exists = os.path.isfile(cfg_name)

        if exists:
            return cfg_name
        else:
            if os.path.isfile('config.cfg'):
                return 'config.cfg'
    except TypeError:
        if os.path.isfile('config.cfg'):
            return 'config.cfg'
    if cfg_file is not None:
        if os.path.isfile(cfg_file):
    #        print(f'Using cfg file at {cfg_file}')
            return cfg_file
    print(f'{cfg_name} and config.cfg do not exist\nTERMINATING')
    sys.exit(0)

def get_cleanup(cleanup_str):
    ''' Turns the cleanup value to a boolean 
    
        determines if the RINEX 2.11 and error files get deleted'''
    if cleanup_str.lower() == 'true':
        return True
    else:
        return False


def get_settings(cfg_file='./config.cfg'):
    ''' Sets up the settings by checking the config file and argument flags

        Argument flags override the config file.

        NOTE: default config file is config.cfg. If that file is not
        in the folder you are running the program in, then you need to use
        the -cfg flag to point to it, or check the readme about 
        creating an executable with it inside
    '''
    parser = argparse_setup(
        argparse.ArgumentParser(description='Create Rinex 3.04 Observation files')
    )
    try:
        args = vars(parser.parse_args())
    except Exception as e:
        print(e)
        parser.print_help()
        sys.exit(0)

    config_name = get_cfg(args['cfg'],cfg_file)
    config = configparser.ConfigParser()
    config.read(config_name)

    
    systems = set_systems(args['systems'], config['SIGNALS']['sv_systems'])
    temp_folder = get_temp_folder(config['SETTINGS']['temp_folder'], args['temp_folder'])
    settings = {
        'input_file' : input_file(input_file(args['in'])),
        'logger' : set_logger(args['logging'], config['SETTINGS']['logging'] ),
        'systems' : systems,
        'supported_filetypes' : get_supported_types(config['SUPPORTED']),
        'temp_folder' : temp_folder,
        'working_dir' : get_working_dir(args['working_dir'], config['SETTINGS']['working_dir']),
        'output_order': get_display_order(config['SIGNALS'],systems),
        'cleanup': get_cleanup(config['SETTINGS']['cleanup']),
        'station_name' : args['station'],
        'quality_check' : args['qc'],
        'output_name' : get_output_name(args['output'], config['SETTINGS']['output_file'])
    }
    for value in config['SUPPORTED'].values(): # Where we add the supported types
        settings[value] = dict()
        for k,v in config[value].items():
            settings[value][k] = v
        settings[value]['working_dir'] = get_working_dir(args['working_dir'], config['SETTINGS']['working_dir'])
        settings[value]['temp_folder'] = temp_folder
        settings[value]['json'] = f'{config["SETTINGS"]["json_dir"]}/{value}.json'
        settings['json'] = config["SETTINGS"]["json_dir"]
    return settings 
