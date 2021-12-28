import pylsl
from .utils import STREAM_INFO_FIELDS, infos_to_dict
from .list import print_infos_line


def find(args): 

	props = {}
	for field in STREAM_INFO_FIELDS:
		try: 
			prop = getattr(args, field)
		except KeyError: 
			pass

		if prop is not None:
			props[field] = prop

	if len(props) == 0: 
		return False

	infos = pylsl.resolve_streams(args.timeout)
	
	found = []
	for info in infos:
		gen_is_ok = (str(getattr(info, field)()) == props[field] for field in props.keys()) 

		if all(gen_is_ok):
			found.append(info)

	if len(found) > 0: 
		infdict = infos_to_dict(found)
		print_infos_line(infdict)

	else: 
		print("No stream found.")