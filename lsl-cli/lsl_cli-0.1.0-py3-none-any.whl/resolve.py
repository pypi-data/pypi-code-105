import pylsl
import argparse
from datetime import datetime
from .utils import *
import sys


def print_infos(infos, fields=STREAM_INFO_FIELDS): 
	fields = {fields} if isinstance(fields, str) else fields

	for field in fields:
		if field not in STREAM_INFO_FIELDS:
			raise ValueError(f"Unkown field: {field}")

	for info in infos: 
		print(info.name())
		for field in fields:
			print(f'  {field}: {getattr(info, field)()}')


INFO_LINE_FIELDS = [
	'type', 'channel_count', 'nominal_srate', 'created_at', 'name'
]
INFO_LINE_FORMAT = {
	'created_at': lambda s: datetime.utcfromtimestamp(float(s)).strftime('%H:%M:%S')
}
INFO_LINE_HEADERS = {
	'type':'type', 'channel_count':'chans', 'nominal_srate': 'rate', 'created_at': 'created', 'name': 'name'
}

def format_field(key, value):
	return '%s'%value if key not in INFO_LINE_FORMAT else INFO_LINE_FORMAT[key](value)

def print_infos_line(infos: dict):
	infos = [
		{k:format_field(k, v) for k, v in info.items() if k in INFO_LINE_FIELDS}
		for info in infos 
	]

	lengths = {k: len(INFO_LINE_HEADERS[k]) for k in infos[0].keys()}
	for i in infos:
		lengths.update(
			{
				k: max(lengths[k], len(i[k])) 
				for k in i.keys()}
		)

	line_format = ''
	for k in INFO_LINE_FIELDS:
		line_format = line_format + '{%s:<%d}  '%(k, lengths[k])

	print(line_format.format(**{k:INFO_LINE_HEADERS[k] for k in INFO_LINE_FIELDS}))
	for i in infos:
		print(line_format.format(**i))



def list(args): 
	if args.all:
		fields = STREAM_INFO_FIELDS
	else: 
		fields = [f for f in STREAM_INFO_FIELDS if getattr(args, f)]

	infos = pylsl.resolve_streams(float(args.timeout))
	if len(infos) == 0:
		return 

	if args.list:
		infodict = infos_to_dict(infos)
		print_infos_line(infodict)

	else: 
		print_infos(infos, fields)

