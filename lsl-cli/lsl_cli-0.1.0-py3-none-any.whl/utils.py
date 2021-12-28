import pylsl


STREAM_INFO_FIELDS = (
	'name',
	'type', 
	'source_id', 
	'channel_count', 
	'channel_format', 
	'nominal_srate', 
	'hostname', 
	'uid', 
	'version', 
	'session_id', 
	'created_at'
)

def infos_to_dict(infos): 
	if not hasattr(infos, '__iter__'):
		infos = [infos]
	return [{
		f: getattr(info, f)() 
		for f in STREAM_INFO_FIELDS
	} for info in infos]

def filter_stream_fields(infos, **fields): 
	for info in infos:
		pass