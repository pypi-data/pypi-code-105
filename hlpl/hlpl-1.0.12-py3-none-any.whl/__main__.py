import configparser
import sys
import os


def get_hlpl_version(case):
    config = configparser.ConfigParser()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_directory, 'setup.cfg')
    config.read(config_file_path)
    if case=='version':
       return config['hlpl']['version']
    if case=='hlpl':
       st='version: '+config['hlpl']['version']+'\n'+'site: '+config['hlpl']['url']+'\n'+'email: '+config['hlpl']['email']+'\n'+'author: '+config['hlpl']['author']+'\n'
       return st
    if case=='version':
       return 'hlpl version: '+config['hlpl']['version']   
    
def main():
    if 'version' in sys.argv:
        print('\n'+get_hlpl_version('version'))
    elif 'docs' in sys.argv:
        print('\n'+'hlpl docs under developement, soon will be released')
    elif 'composer' in sys.argv:
        print('\n'+'hlpl composer under developement, soon will be released')
    elif 'templater' in sys.argv:
        print('\n'+'hlpl templaterunder developement, soon will be released')
    elif 'transcriber' in sys.argv:
        print('\n'+'hlpl transcriberunder developement, soon will be released')
    elif 'press' in sys.argv:
        print('\n'+'hlpl pressunder developement, soon will be released')
    elif 'character' in sys.argv:
        print('\n'+'hlpl characterunder developement, soon will be released')
    elif 'photographer' in sys.argv:
        print('\n'+'hlpl photographerunder developement, soon will be released')
    elif 'graphics' in sys.argv:
        print('\n'+'hlpl graphicsunder developement, soon will be released')
    else:
        print('\n'+get_hlpl_version('hlpl'))