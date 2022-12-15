import sys
def find_type(Log: None, inputfile : str, supported_types) -> str:
    
    ''' Identifies which vendor the raw data file is from 

        Args:
            Log
                Function to provide consistant, layered output
            inputfile
                Name of the inputfile
            supported_types
                a key-value pair representing the supported file types. Can
                be found in config file.
                key
                    3 digit identifier. For YY_ (YY = year, _ is 
                    vendor identifier) it checks if the first two
                    characters are numbers, and replaces them with "y"s
                    if they are.
                value
                    The name of a data type that is supported. 
        Returns:
            The value associated with the key matching 
    '''
    type_keys = [key for key in supported_types.keys()]
    extensions = inputfile.split('.')
    
    for file_segment in extensions:
        if len(file_segment) == 3:
            try:
                # This will catch YY_ patterns used by several receivers
                int(file_segment[0:2])
                input_type = supported_types['yy'+file_segment[2]]
                return input_type
            except:
                pass
        if file_segment in type_keys:
            return supported_types[file_segment]
    Log('E', f'<{inputfile}> not a supported filetype')
    sys.exit(9)

