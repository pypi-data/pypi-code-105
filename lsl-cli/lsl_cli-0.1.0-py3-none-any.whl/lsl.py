from .utils import *
from .list import list
from .echo import echo
from .show import show
from .find import find
import argparse



def complete(args): 
	import subprocess
	import os
	path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(path)

	if args.zsh:
		_args = ['zsh']
	elif args.bash:
		_args = ['bash']
	else: 
		_args = []
	subprocess.call([os.path.join(path, 'extra/lsl_complete_script.sh')] + _args, env=os.environ.copy())
	

def main():
	parser = argparse.ArgumentParser()

	subparser = parser.add_subparsers(dest='command')

	complete_parser = subparser.add_parser('complete')
	complete_parser_group = complete_parser.add_mutually_exclusive_group()
	complete_parser_group.add_argument('--zsh', '-z', action='store_true', dest='zsh')
	complete_parser_group.add_argument('--bash', '-b', action='store_true', dest='bash')

	complete_parser.set_defaults(func=complete)

	list_parser = subparser.add_parser('list')
	list_parser.add_argument('--all', '-a', dest='all', action='store_true')
	list_parser.add_argument('--list', '-l', dest='list', action='store_true')
	list_parser.add_argument('--timeout', dest='timeout', type=float, default=0.05)

	for field in STREAM_INFO_FIELDS:
		list_parser.add_argument(f'--{field}', dest=field, action='store_true', help=f"Display stream {field}")
	
	list_parser.set_defaults(func=list)

	echo_parser = subparser.add_parser('echo', description="Print to screen messages from a stream.")
	echo_parser.add_argument('name', help='Stream name')
	echo_parser.add_argument('--timeout', dest='timeout', type=float, default=0.05)

	echo_parser.set_defaults(func=echo)

	show_parser = subparser.add_parser('show')
	show_parser.add_argument('name', help='Stream name')
	show_parser.add_argument('--timeout', dest='timeout', type=float, default=0.05)

	show_parser.set_defaults(func=show)

	find_parser = subparser.add_parser('find')
	for field in STREAM_INFO_FIELDS:
		find_parser.add_argument(f'--{field}', dest=field, type=str, help=f"Display stream {field}")
	find_parser.add_argument('--timeout', dest='timeout', type=float, default=0.05)
	find_parser.set_defaults(func=find)

	args = parser.parse_args()
	if args.command is None:
		parser.print_help()
	else: 
		res = args.func(args)
		if res is False:
			parser.print_help()



