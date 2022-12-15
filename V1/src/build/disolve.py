from collections import deque
from math import ceil
''' Disolve Data files into managable blobs

    The thought behind this is that if we generate a dict containing 
    all the data needed to create a rinex 3 file, then we can just 
    build that rinex 3 file. This file contains the functions used
    to format the data from RINEX 2.11 OBS files.

    Get header
    get signals from the header
    extract data    
        first line
            get date
            get satallite count
            satallite_cnt * signal_cnt = data_pnt_cnt
                5 data points per line
                while signal_cnt > 0:
                    get line
                    consume signals
                    -5 to signal count
                    repeat loop
    '''

def get_header(Log, dq : deque) -> dict:
    ''' Gets the header information from the deque data structure
    
        Args:
            Log
                Logging function for uniform layered output
            dq
                deque data structure. Chosen due to O(1) performance
                on removing objects from the ends vs O(n) for lists
            filename

    
    '''
    header = dict()
    while len(dq) > 0:
        line = dq.popleft()
        key = f'{line[60:]}'.strip('\n')
        value = f'{line[:60]}'
        if key in header.keys():
            if type(header[key]) is str:
                header[key] = [header[key]]
            header[key].append(value)
        else:
            header[key] = value
        if 'END OF HEADER' in line:
            Log('D', 'Header exhausted')
            Log('D', f'{len(dq)} Lines of data left after removing header')
            return header
    Log('E', 'The deque was only header??')
    sys.exit(5)

def get_obs(Log, header: dict):
    for line in header:
        if 'TYPES OF OBSERV' in line:
            signals = header[line]
    if type(signals) == list:
        signals = ''.join(signals)
    signals = list(filter(None,signals.split(' ')))
    signals = signals[1:]
    return signals

def get_epoch_time(Log, line):
    ''' gets the date and time 
    
        Very specific formatting for output. Warning if 
        you try to reformat
        '''
    # Log('D', 'Extracting Date and time from epoch')
    tokens = list(filter(None,line.split(' ')))
    date = [f'{int(token):02}' for token in tokens[:5]]
    date.extend([f'{tokens[5]:>10}', f'{tokens[6]:>2}'])
    time = ' '.join(date)
    return time

def get_sv_count(Log, line):
    ''' gets the number of SV's '''
    sv_token = list(filter(None,line.split(' ')))[-1]
    # Log('D', f'{sv_token}')
    get_numbers = list()
    for char in sv_token:
        if char.isdigit():
            get_numbers.append(char)
        else:
            break
    sv_count = int(''.join(get_numbers))
    # Log('D', f'sv count = {sv_count}')
    return sv_count

def get_sv_list(Log, lines_sv: list):
    ''' creates a list of the sv's from this epoch '''
    # process the lines
    lines = ''.join(list(filter(None, (''.join(lines_sv).split(' ')))))
    sv = ''
    sv_list = list()
    for char in lines:
        if char.isalpha():
            if len(sv) == 3:
                sv_list.append(sv)
            sv = ''
        sv += char
    sv_list.append(sv)
    return sv_list

def get_sv_obs(Log, obs, dq):
    ''' creates a dict of the observations belonging to a certain SV '''
    obs_per_line = 5
    all_obs = dict()
    for idx, ob in enumerate(obs):
        if idx%5 == 0:
            line = dq.popleft().strip('\n')
        step = idx%5
        # Log('D', f'{ob} {line[16*step:16*(step+1)]}')
        all_obs[ob] = line[16*step:16*(step+1)]
    return all_obs

def get_data_rnx211(Log, dq: deque, signals: list) -> dict:
    ''' Creates a dict from all the data in the dq '''
    Epoch_data = dict()
    # get the date
    while len(dq) > 0:
        line = dq.popleft() # gets the line containing date and SV list Start
        line = line.strip('\n')
        epoch_time = get_epoch_time(Log, line)
        Epoch_data[epoch_time] = dict()
        sv_count = get_sv_count(Log, line)
        lines_sv = [line.split(' ')[-1]]
        while len(lines_sv) < ceil(sv_count/12):
            lines_sv.append(dq.popleft().strip('\n'))
        sv_list = get_sv_list(Log, lines_sv)
        if len(sv_list) != sv_count:
            Log('E', f'Sv count is messed up dude {len(sv_list)} vs {sv_count}')
        lines_per_sv = ceil(len(signals)/5)
        for sv in sv_list:
            Epoch_data[epoch_time][sv] = get_sv_obs(Log, signals, dq)
    return Epoch_data


def extract(Log, raw_files: list, settings: dict) -> dict:
    ''' Creates a dict containing header data and observation data'''
    Files = dict() # Key is file_name, value is deque of lines
    Data = dict() # Key is Epoch, value is Dict's representing the SV's
    Header = dict() # Key is file name, value is header information
    for file_name in raw_files:
        Log('D', f'Parsing {file_name}')
        with open(file_name, 'r') as F:
            Files[file_name] = deque()
            # if 'meta' in file_name:
            #     print(file_name)

            for line in F: # read it all into a deque to avoid possible file corruption
                Files[file_name].append(line)

            Log('D', f'{len(Files[file_name])} lines taken into Data Deque')
    for dq in Files:
        Log('D', f'Getting header information from {dq}')
        if 'meta' in dq:
            Header['meta'] = Files[dq]
            continue
        Header[dq] = get_header(Log, Files[dq])
        signals = get_obs(Log, Header[dq])
        Data[dq] = get_data_rnx211(Log, Files[dq], signals)
    return {'Data': Data, 'Header' : Header}




