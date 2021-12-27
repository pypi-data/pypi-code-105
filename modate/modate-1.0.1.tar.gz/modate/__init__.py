import click
import platform
from datetime import datetime
from re import match

@click.command()
@click.option('-f', '--filepath', prompt=False, help='Filepath of the file(s) to modify. Accepts wildcard arguments.')
@click.option('-d', '--date', prompt=False, help='Datetime to use.')
@click.option('-df', '--date_format', prompt=False, help='Specify format in which the datetime is stated in the filename. Use strftime directives.')
@click.option('-c', '--created', is_flag=True, help='Change the "created" datetime.')
@click.option('-m', '--modified', is_flag=True, help='Change the "modified" datetime.')
@click.option('-a', '--accessed', is_flag=True, help='Change the "last opened" datetime.')


def main(filepath,date,date_format,created,modified,accessed):
    # Convert input date to datetime
    if date is not None:
        date = todatetime(date)
        print('Using date: %s for file %s' % date.strftime('%Y-%b-%d %H:%M:%S'),filepath.split('/')[-1])
    elif date_format is not None:
        pass # Needs to be handled separately for each file and each system
    else:
        raise(click.BadParameter("No date passed.\n Please declare a date to modify.\n Use 'modate --help' to check the functionality."))

    if platform.system() == 'Windows':
        from modate import win
        win.main(filepath,date,date_format,created,modified,accessed)
    elif platform.system() == 'Darwin':
        from modate import mac
        mac.main(filepath,date,date_format,created,modified,accessed)
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