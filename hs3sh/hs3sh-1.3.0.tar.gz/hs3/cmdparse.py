# The MIT License (MIT)
#
# Copyright (c) 2016-2021 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import argparse
import sys


class ArgumentParseError(Exception):
    """An error happened during argparse."""
    pass

class myArgumentParser(argparse.ArgumentParser):
    """
    We need to block ArgumentParser from exiting the code ;-)
    """
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        raise ArgumentParseError

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self._print_message(f'{self.prog}: error: {message}\n')
        raise ArgumentParseError


class CmdParser():
    """
    Class to parse command parameters.
    """

    def __init__(self, hs3shobj):
        """
        :param hs3shobj:  the cmd object
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug('--> initializing cmdparser...')

        # initialize parsers
        self.parsers = {}
        for func in [x for x in self.__dir__() if '__parser_' in x]:
            self.parsers[func[func.rfind('_')+1:]] = eval(f'self.{func}()')
        self.logger.debug(f'--> initialized cmdparsers: {self.parsers}')


    def parse(self, cmd, args):
        """
        Submit args to the correct prepared parser.

        :param cmd:   the command
        :param args:  the arguments (string)
        :return:      the resulting ArgumentParser Namespace object
        """
        self.logger.debug(f'--> called {cmd} parser with {args}')

        # for some commands, we need to insert '--' after cmd to keep argparse from
        # looking at eventual arguments
        if cmd in ['debug', 'time']:
            _args = args.split()
            if len(_args) > 1:
                _args.insert(1, '--')
                args = ' '.join(_args)

        try:
            ret = self.parsers[cmd].parse_args(args.split())
            self.logger.debug(f'--> parse result: {ret}')
            return ret
        except ArgumentParseError as e:
            self.logger.debug(f'--> parse raised {e}')
            raise


    def help(self, cmd):
        """
        Print help for a parser.

        :param cmd:   the command
        """
        self.logger.debug(f'--> called {cmd} parser to print help')
        self.parsers[cmd].print_help()


    # The following methods are creating the argument parsers for all the commands
    def __parser_attach(self):
        'attach <bucket_name>\n' \
        '    Attaches the bucket to be used by further commands. Think of\n' \
        '    change directory...'
        self.logger.info('--> called "__parser_attach"')
        p = myArgumentParser(prog='attach', exit_on_error=False,
                             description='Attach the bucket to work with.')
        p.add_argument(dest='bucket', action='store',
                       help='the bucket\'s name')
        return p

    def __parser_bucket(self):
        'bucket [-c|-cv|-r|-v] bucketname\n' \
        '    create or remove a bucket\n' \
        '    -c create <bucketname>\n' \
        '    -r remove bucket (needs to be empty)\n' \
        '    -v toggle versioning\n' \
        '    without any flags, the bucket\'s versioning status is shown'
        self.logger.info('--> called "__parser_bucket"')
        p = myArgumentParser(prog='bucket', exit_on_error=False,
                             description='Create or remove a bucket, toggle versioning, '
                                         'show versioning setting when no options are set.')
        g = p.add_mutually_exclusive_group()
        g.add_argument('-c', dest='create', action='store_true', default=False,
                       help='create BUCKET')
        g.add_argument('-r', dest='remove', action='store_true', default=False,
                       help='remove BUCKET')
        p.add_argument('-v', dest='versioning', action='store_true', default=False,
                       help='toggle versioning')
        p.add_argument(dest='bucket', action='store',
                       help='the bucket\'s name')

        return p

    def __parser_bye(self):
        'Exit hs3sh gracefully.'
        self.logger.info('--> called "__parser_bye"')
        p = myArgumentParser(prog='bye', exit_on_error=False,
                             description='Exit hs3sh gracefully.')
        return p

    def __parser_clear(self):
        'clear\n'\
        '    Clear screen\n'
        self.logger.info('--> called "__parser_clear"')
        p = myArgumentParser(prog='clear', exit_on_error=False,
                             description='Clear screen.')
        return p

    def __parser_config(self):
        'set config_item value\n' \
        '    known config items:\n' \
        '    mpu_size    : MultiPartUpload part size in MB\n' \
        '    mpu_threads : no. of concurrent uploads\n'
        self.logger.info('--> called "__parser_config"')
        p = myArgumentParser(prog='config', exit_on_error=False,
                             description='Get or set configuration item values')
        p.add_argument('-s', dest='configitem', choices=['mpu_size', 'mpu_threads'],
                          help='the configuration items to set')
        p.add_argument('-v', dest='value', action='store', type=int, nargs='?',
                          help='the (integer) value to set.')
        return p

    def __parser_connect(self):
        'connect <profile_name>\n' \
        '    Connect to an S3 endpoint using profile <profile_name>\n' \
        '    from ~/.hs3sh.conf or ./.hs3sh.conf'
        self.logger.info('--> called "__parser_connect"')
        p = myArgumentParser(prog='connect', exit_on_error=False,
                             description='Connect to an S3 endpoint using profile profile.')
        p.add_argument(dest='profile',
                          help='a profile configured in the config file')
        return p

    def __parser_cp(self):
        'cp [-v version_id] source target ["metakey:metavalue"]*\n' \
        '    Request the S3 service to perform a server-side copy of (a '\
        'defined\n' \
        '    version_id of) source to target object, replacing eventually\n' \
        '    existing source metadata pairs with the named metadata pairs,\n' \
        '    if given; else copy the existing metadata pairs, along with the\n'\
        '    object.\n\n' \
        '    You can use the copy command to copy the source object to\n' \
        '    itself to create a new version of the source object with\n' \
        '    changed metadata pairs.'
        self.logger.info('--> called "__parser_cp"')
        p = myArgumentParser(prog='cp', exit_on_error=False,
                             description='Request the S3 service to server-side '
                                         'copy an object.',
                             epilog='')
        p.add_argument('-v', dest='versionid', required=False, default=None,
                          help='sourceobject\'s versionId. Will create a copy of '
                               'the specified object version')
        p.add_argument(dest='sourceobject',
                          help='name (key) of the object to copy')
        p.add_argument(dest='targetobject',
                          help='name (key) of the target')
        p.add_argument(dest='meta', action='store', nargs='*',
                       help='format is: "key:value". Proving meta will replace '
                            'eventually existing metadata in sourceobject with what '
                            'is given as meta in targetobject')
        return p

    def __parser_debug(self):
        'debug [cmd [args]]\n' \
        '    Without "cmd [args]", toggle debug mode,\n' \
        '    with "cmd [args]", toggle debug mode for that command, only.'
        self.logger.info('--> called "__parser_debug"')
        p = myArgumentParser(prog='debug', exit_on_error=False,
                             description='Without "cmd [args]", toggle debug mode globally, '
                                         'with "cmd [args]", toggle debug mode for that '
                                         'command, only.')
        p.add_argument(dest='command', action='store', nargs='?',
                       help='the command to run')
        p.add_argument(dest='args', action='store', nargs='*',
                       help='(optional) arguments')
        return p

    def __parser_get(self):
        'get [-m] [-v version_id] object [localfile]\n' \
        '    Get (read) an object and _print it.\n' \
        '    -m request MultiPartDownload,\n' \
        '    -v get object version instead of the latest version\n' \
        '    If localfile is specified, store the object to it.'
        self.logger.info('--> called "__parser_get"')
        p = myArgumentParser(prog='get', exit_on_error=False,
                             description='Get (download) an object.')
        p.add_argument('-m', dest='mpu', action='store_true', required=False, default=False,
                          help='request a multipart download')
        p.add_argument('-v', dest='versionid', required=False, default=None,
                          help='sourceobject\'s versionId. Will download '
                               'the specified version')
        p.add_argument(dest='object', action='store',
                       help='name (key) of the object to download')
        p.add_argument(dest='localfile', action='store', nargs='?', default='',
                       help='name of the local file to store the download (if not '
                            'given, the source object\'s name will be used')
        return p

    def __parser_getbl(self):
        'getbl <bucket>\n' \
        '    Get (read) the bucket location for <bucket>.'
        self.logger.info('--> called "__parser_getbl"')
        p = myArgumentParser(prog='getbl', exit_on_error=False,
                             description='Get the location for bucket.')
        p.add_argument(dest='bucket', action='store',
                       help='the bucket\'s name')
        return p

    def __parser_lcd(self):
        'lcd [local-directory]\n'\
        '    change the local working directory to local-directory (or to\n'\
        '    home directory, if local-directory isn\'t given)'
        self.logger.info('--> called "__parser_lcd"')
        p = myArgumentParser(prog='lcd', exit_on_error=False,
                             description='Change the local working directory to localdirectory '
                                         '(or to home directory, if localdirectory isn\'t given).')
        p.add_argument(dest='localdirectory', action='store', default='', nargs='?',
                       help='the local directory')
        return p

    def __parser_lls(self):
        'lls [local-path]\n'\
        '    list contents of local path'
        self.logger.info('--> called "__parser_lls"')
        p = myArgumentParser(prog='lls', exit_on_error=False,
                             description='List contents of local path.')
        p.add_argument(dest='localdirectory', action='store', default='', nargs='?',
                       help='the local directory to be listed')
        return p

    def __parser_lpwd(self):
        'lpwd\n'\
        '    Print the local working directory.'
        self.logger.info('--> called "__parser_lpwd"')
        p = myArgumentParser(prog='lpwd', exit_on_error=False,
                             description='Print the local working directory.')
        return p

    def __parser_ls(self):
        self.logger.info('--> called "__parser_ls"')
        p = myArgumentParser(prog='ls', exit_on_error=False,
                             description='List the objects within the active bucket.')
        p.add_argument('-a', dest='acl', action='store_true', default=False,
                       help='print object acls')
        p.add_argument('-e', dest='etag', action='store_true', default=False,
                       help='print object etags')
        p.add_argument('-m', dest='metadata', action='store_true', default=False,
                       help='print object metadata')
        p.add_argument('-v', dest='versions', action='store_true', default=False,
                       help='print object versions')
        p.add_argument(dest='prefix', action='store', nargs='?', default='',
                       help='list objects starting with the prefix')
        return p

    def __parser_lsb(self):
        self.logger.info('--> called "__parser_lsb"')
        p = myArgumentParser(prog='lsb', exit_on_error=False,
                             description='List the buckets available through the connected endpoint.')
        p.add_argument('-a', dest='acl', action='store_true', default=False,
                       help='print bucket acls')
        return p

    def __parser_lsp(self):
        self.logger.info('--> called "__parser_lsp"')
        p = myArgumentParser(prog='lsp', exit_on_error=False,
                             description='Show the configured profiles.')
        return p

    def __parser_profile(self):
        self.logger.info('--> called "__parser_profile"')
        p = myArgumentParser(prog='profile', exit_on_error=False,
                             description='Edit the configuration file(s).',
                             epilog='This will start `vi` with the selected config file.')
        return p

    def __parser_progress(self):
        self.logger.info('--> called "__parser_progress"')
        p = myArgumentParser(prog='progress', exit_on_error=False,
                             description='Toggle showing a progressmeter on/off.')
        return p

    def __parser_put(self):
        'put [-m] localfile object ["metakey:metavalue"]*\n' \
        '    Put (store) localfile as object into the attached bucket,\n' \
        '    adding metadata pairs, if specified.\n' \
        '    -m will try to do a multi-part put.'
        self.logger.info('--> called "__parser_put"')
        p = myArgumentParser(prog='put', exit_on_error=False,
                             description='Put (upload) "sourcefile" as "targetobject" into '
                                         'the attached bucket, adding metadata pairs '
                                         'if specified.')
        p.add_argument('-m', dest='mpu', action='store_true', default=False,
                       help='do a multi-part upload, if ever possible.')
        p.add_argument(dest='sourcefile', action='store',
                       help='name of the local (source) file to upload.')
        p.add_argument(dest='targetobject', action='store',
                       help='name of the object in the target bucket.')
        p.add_argument(dest='meta', action='store', nargs='*',
                       help='format is: "key:value"')
        return p

    def __parser_rm(self):
        'rm object [version_id]\n' \
        '    Delete object (or it\'s version_id) from the attached bucket.'
        self.logger.info('--> called "__parser_rm"')
        p = myArgumentParser(prog='rm', exit_on_error=False,
                             description='Delete object from the attached bucket.')
        p.add_argument(dest='object', action='store',
                       help='name of the object to remove.')
        p.add_argument(dest='version_id', action='store', nargs='?',
                       help='id of the object version to remove')
        return p

    def __parser_run(self):
        'run <script>\n' \
        '    Run a batch of commands stored in file <script>.'
        self.logger.info('--> called "__parser_run"')
        p = myArgumentParser(prog='run', exit_on_error=False,
                             description='Run a batch of commands stored in commandfile.\n'
                                         'A commandfile is just a plain sequential list of '
                                         'commands to be run, as you would enter them into'
                                         'an interactive session. Not ending it with "bye" will leave'
                                         'the interactive session open.')
        p.add_argument(dest='commandfile', action='store',
                       help='name of the commandfile to run.')
        return p

    def __parser_status(self):
        'status\n' \
        '    Show the session status (the connected endpoint and the\n' \
        '    attached bucket)'
        self.logger.info('--> called "__parser_status"')
        p = myArgumentParser(prog='status', exit_on_error=False,
                             description='Show the session status (the connected endpoint '
                                         'and the attached bucket).')
        return p

    def __parser_time(self):
        'time <command args>\n' \
        '    measure the time <command> takes to complete'
        self.logger.info('--> called "__parser_time"')
        p = myArgumentParser(prog='time', exit_on_error=False,
                             description='Measure the time command takes to complete.')
        p.add_argument(dest='command', action='store',
                       help='the command to run')
        p.add_argument(dest='args', action='store', nargs='*',
                       help='(optional) arguments')
        return p

    def __parser_url(self):
        'url [-e minutes] object\n' \
        '    Generate a pre-signed URL to access object\n' \
        '    -e set the expiration time for the URL to minutes\n' \
        '       (defaults to 60 minutes)\n' \
        '    -u generates an upload URL instead of a download URL'
        self.logger.info('--> called "__parser_url"')
        p = myArgumentParser(prog='url', exit_on_error=False,
                             description='Generate a pre-signed URL to access an object.')
        p.add_argument('-m', dest='minutes', action='store', type=int,
                       required=False, default=60,
                       help='set the expiration time for the URL to MINUTES (defaults to 60 minutes)')
        p.add_argument('-u', dest='upload', action='store_true', default=False,
                       help='generates an upload URL instead of a download URL')
        p.add_argument(dest='object', action='store',
                       help='the object name (key)')
        return p

