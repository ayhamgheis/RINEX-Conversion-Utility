from src import setup, build, postprocess


def run(config = None):
    # Parse the config files and argument variables. Creates a dict of settings
    settings = setup.settings.get_settings()
    # Set up the logger. Creates a logger object
    Log = setup.logger.get_logger(settings['logger'])
    Log('D', settings)
   
    #identify filetype using 3 digit suffix
    input_type = build.filetype.find_type(Log, settings['input_file'], settings['supported_filetypes'])

    # create the raw file that is readable by tecq, and return its name
    raw_files = build.process.make_raw_file(Log, settings['input_file'], settings[input_type])
    
    # create the tecq 2.11 files according to the settings
    # extract a dict representing all observations from all Rinex 2.11 files
    data = build.disolve.extract(Log, raw_files, settings[input_type])

    # Create a Rinex 3.05 observation file from the data dict
    rnx3 = build.construct.create_305(Log, data, settings[input_type], settings['output_order'], settings['output_name'], settings['json'],settings['station_name'])

    Log('I', f'Processed {settings["input_file"]}')

    
    if settings['quality_check']: 

        Log('I',f'Quality checking output file: {rnx3}')
        output_qc = f'{rnx3}.qc'
        command = f'gfzrnx -finp {rnx3} -chk -kv {output_qc}'
        build.process.sp(Log, command)
        print(output_qc)
   
    if settings['cleanup']:
        Log('I', f'Removing generated RINEX 2.11 directory {settings["temp_folder"]}')
        postprocess.cleanup.temp_folder(Log, settings['temp_folder'], settings['working_dir'])
    


if __name__ == '__main__':
    run()
