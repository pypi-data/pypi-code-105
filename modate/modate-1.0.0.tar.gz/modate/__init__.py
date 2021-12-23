import click
import platform
from datetime import datetime

@click.command()
@click.option('-f', '--filepath', prompt=False, help='Filepath of the file(s) to modify. Accepts wildcard arguments.')
@click.option('-d', '--date', prompt=False, help='Date to be modified')
# @click.option('-df', '--date_in_filename', prompt=False)
@click.option('-c', '--created', is_flag=True, help='Change the "created" datetime')
@click.option('-m', '--modified', is_flag=True, help='Change the "modified" datetime')
@click.option('-a', '--accessed', is_flag=True, help='Change the "last opened" datetime')

def main(filepath,date,created,modified,accessed):
    # Convert input date to datetime
    date = todatetime(date)
    if platform.system() == 'Windows':
        from . import win
        win.main(filepath,date,created,modified,accessed)
    elif platform.system() == 'Darwin':
        from . import mac
        mac.main(filepath,date,created,modified,accessed)
    else:
        print('The tool is not yet available for this platform')


def todatetime(date):
    try:
        date = datetime.strptime(date, '%Y%m%d_%H%M%S')
    except:
        raise(click.BadParameter("Date '%s' has bad format" % date))
    return(date)


if __name__ == '__main__':
    main()