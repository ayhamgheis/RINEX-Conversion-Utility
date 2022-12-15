import subprocess, sys, os

## will address use of subprocess module and potential security concerns

def teqc(Log, input_file, arguments):
    ''' Creates RINEX 2.11 files using teqc 

        Args:
            Log
                Logging function to provide uniform, layered output
            input_file
                The input file 
            arguments
                dictionary containing
                    temp_folder
                        Directory where rinex 2.11 observation files will be
                        created by calls to teqc. Will be created if it does
                        not exist.
                    working_dir
                        Directory where rinex 3.05 observation file and
                        temp_folder will be created. 
                    arguments
                        list of arguments to be used by teqc. From config file.
        Returns:
            interm_file_names
                The names of 
    '''
    sp(Log, f'which teqc')
    arg_variations = arguments['arguments'].split('|')
    working_dir = arguments['working_dir']
    temp_folder = arguments['temp_folder']
    interm_file_names = list()
    Log('D', f'Running teqc {arg_variations}')
    input_file_name = input_file.split('.')[0].split('/')[-1]
    if temp_folder not in sp(Log, f'ls {working_dir}'):
        sp(Log, f'mkdir {working_dir}/{temp_folder}')
        Log('D', f'{temp_folder} created')
    else:
        Log('D', f'{temp_folder} exists')
    temp_folder = f'{working_dir}/{temp_folder}'
    for variation in arg_variations:
        teqc_arg = ' '.join(variation.split(','))
        interm_file = teqc_arg.lower()
        interm_file = input_file_name + '.' + 'Wo_'.join('W_'.join('.'.join(interm_file.split(' ')).split('+')).split('-'))
        output_filename = f"{temp_folder}/{interm_file}"
        error_filename = f"{temp_folder}/err.log"
        if 'meta' in output_filename:
            sp(Log, f"teqc +err {error_filename} {teqc_arg} {input_file} > {output_filename}")
            sp(Log, f"teqc +err {error_filename} +qc {input_file} | grep xyz >> {output_filename}")
        else:
            placeholder = sp(Log, f"teqc +err {error_filename} {teqc_arg} +obs {output_filename} {input_file}")
        # sp(Log, f"teqc +err err.log {teqc_arg} +obs {working_dir}/{temp_folder}/{interm_file} {input_file}")

        interm_file_names.append(output_filename)
    return interm_file_names


def sp(Log, cmd : str) -> str:
    ''' Wraps subprocess calls to reduced code

        Args:
            Log
                logging object for logging information
            cmd
                command to be executed through the subprocess module
    
        Returns:
            output
                string representing the output of the subprocess call
    '''
    status, output = subprocess.getstatusoutput(cmd)
    if status == 0:
        Log('D', f'<{cmd}> successful')
        return output
    else:
        Log('E', f'Subprocess call ({cmd}) failed with code {status} <{os.strerror(status)}>')
        if status == 255:
            Log('E', f'Error 255 can be non-existing file, check filename')
        sys.exit(status)



def make_raw_file(Log, input_file, input_type):
    Log('D', f'{input_file} - {input_type}')
    return data_processing_switch[input_type['steps']](Log, input_file, input_type)


data_processing_switch = {
    'teqc_all' : teqc
}
