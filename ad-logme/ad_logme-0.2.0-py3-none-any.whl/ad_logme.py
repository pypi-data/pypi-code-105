from datetime import datetime
import enum

def get_datetime_now():
  return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

class LogType(enum.Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'
    FATAL = 'FATAL'


class LogWriter():
    def __init__(self, filepath, encoding):
        self.filepath = filepath
        self.encoding = encoding
        self.create_logfile()

    def create_logfile(self):
        with open(self.filepath, "x", encoding=self.encoding) as f:
            f.write("")
    
    def debug(self, string):
        with open(self.filepath, "a", encoding=self.encoding) as f:
            f.write("DEBUG,%s,%s" % (get_datetime_now(), string))
        print("[DEBUG] - %s\n%s\n" % (get_datetime_now(), string))
    
    def info(self, string):
        with open(self.filepath, "a", encoding=self.encoding) as f:
            f.write("INFO,%s,%s" % (get_datetime_now(), string))
        print("[INFO] - %s\n%s\n" % (get_datetime_now(), string))
    
    def warn(self, string):
        with open(self.filepath, "a", encoding=self.encoding) as f:
            f.write("WARN,%s,%s" % (get_datetime_now(), string))
        print("[WARN] - %s\n%s\n" % (get_datetime_now(), string))
    
    def error(self, string):
        with open(self.filepath, "a", encoding=self.encoding) as f:
            f.write("ERROR,%s,%s" % (get_datetime_now(), string))
        print("[ERROR] - %s\n%s\n" % (get_datetime_now(), string))
    
    def fatal(self, string):
        with open(self.filepath, "a", encoding=self.encoding) as f:
            f.write("FATAL,%s,%s" % (get_datetime_now(), string))
        print("[FATAL] - %s\n%s\n" % (get_datetime_now(), string))

    
def debug(string):
    print("[DEBUG] - %s\n%s\n" % (get_datetime_now(), string))

def info(string):
    print("[INFO] - %s\n%s\n" % (get_datetime_now(), string))

def warn(string):
    print("[WARN] - %s\n%s\n" % (get_datetime_now(), string))

def error(string):
    print("[ERROR] - %s\n%s\n" % (get_datetime_now(), string))

def fatal(string):
    print("[FATAL] - %s\n%s\n" % (get_datetime_now(), string))
