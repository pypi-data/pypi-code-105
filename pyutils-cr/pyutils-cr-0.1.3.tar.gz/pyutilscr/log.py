import subprocess
import json
import logging

def log(executed_file:str,dump_file_name:str):
	proc = subprocess.Popen(["python3",executed_file],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	f=open(dump_file_name,"w+")
	f.write(proc.communicate(input=None, timeout=None)[0].decode("utf-8"))
	f.close()
def extract_log(file,json_:bool=False):
	if json_ == False:
		try:
			with open(file,"r+") as f:
				store = f.read()
				return store
		except Exception as error:
			logging.error(error)
	if json_ == True:
		try:
			f = open(file, "r+")
			fjson = json.load(f)
			return fjson
		except Exception as error:
			logging.error(error)