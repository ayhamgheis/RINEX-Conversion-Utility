import logging
import sys 
class rnxlogger:
    def __init__(self, log_settings=None):
        log_setup = logging.getLogger()
        log_setup.handlers = []
        stdoutH = logging.StreamHandler(sys.stdout)
        stdoutH.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        )
        log_setup.addHandler(stdoutH)
        self.Log = log_setup

    def set_lvl(self, lvl):
        ''' Sets the logging level to be used

            Different logging levels will determine how verbose the output
            data is. See https://docs.python.org/3.6/library/logging.html
            for more information.

            ARGS
                lvl     The level at which to log. One of
                            ERROR
                            INFO
                            DEBUG
                        with DEBUG being the most verbose
        '''
        self.Log.setLevel(lvl)
        self.log('D',f'Logging level set to {lvl}')

    def log(self, lvl, msg):
        ''' Outputs information

            Instead of printing to stdout, we use a logger which allows for different
            levels of output. Default can be set in Rnx3.cfg, or changed at runtime with 
            \'-logging\' flag 

            ARGS
                lvl     The level that we wish to log at
                            E : Error
                            W : Warning
                            D : Debug

                msg     either a string or list of strings that we wish to log
        '''
        out = {
            'E' : self.Log.error,
            'W' : self.Log.warning,
            'D' : self.Log.debug,
            'I' : self.Log.info
        }
        try:
            if type(msg) == type(list()):
                for item in msg:
                    out[lvl](item)
            else:

                out[lvl](msg)
        except Exception as e:
            raise e    



def get_logger(log_settings : str):
    logger = rnxlogger()
    logger.set_lvl(log_settings)
    return logger.log
