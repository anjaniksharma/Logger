import os, sys, re, errno,logging
import time, datetime
from logging.handlers import TimedRotatingFileHandler

class NPDLogger(logging.getLoggerClass()):
        def __init__(self,log_file_name = None, log_severity_level = None, console = None):
                if not log_severity_level:
                        self.log_severity_level = 'debug'
                else:
                        if log_severity_level.lower() not in ['debug','info','warning','error','critical']:
                                raise NameError("NPDLogger -> Invalid Severity Level: %s" %log_severity_level)
                        else:
                                self.log_severity_level = log_severity_level

                if not log_file_name:
                        raise NameError("NPDLogger -> Log file name not defined!!")
                else:
                        work_serial = os.getenv('WORK_SERIAL')
                        if not work_serial:
                                raise NameError("NPDLogger -> .profile parameter WORK_SERIAL not set")
                        try: os.makedirs(work_serial + '/ml_logs')
                        except OSError, e:
                                if e.errno != errno.EEXIST:
                                        raise NameError("NPDLogger ->  OS Error in Creating ml log directory %s_/ml_logs" %(work_serial))
                        self.log_file_name = work_serial + '/ml_logs/' + log_file_name
                if not console:
                        self.console = False
                else:
                        self.console = True
		self.logger = None

        def log(self):
		
                self.logger = logging.getLogger(self.log_file_name)
                self.logger.setLevel(eval('logging.' + self.log_severity_level.upper()))
                #formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(funcName)s:%(lineno)d -> %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
		formatter = logging.Formatter('%(levelname)7s [%(asctime)s] [%(filename)s %(threadName)s] [%(funcName)s] [%(lineno)d]: %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
		fh = None
		#fh = logging.FileHandler(self.log_file_name + "_" + time.strftime('%m%d%Y')+ '.log')
		fh = TimedRotatingFileHandler(self.log_file_name + "_" + time.strftime('%m%d%Y')+ '.log',when='midnight')
                fh.setLevel(eval('logging.' + self.log_severity_level.upper()))
                fh.setFormatter(formatter)
		self.logger.handlers = []
                self.logger.addHandler(fh)
                if self.console == True:
			ch = None
                        ch = logging.StreamHandler()
                        ch.setLevel(eval('logging.' + self.log_severity_level.upper()))
                        ch.setFormatter(formatter)
                        self.logger.addHandler(ch)
                return self.logger
		
