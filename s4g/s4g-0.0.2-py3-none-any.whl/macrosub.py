from importlib import import_module
import traceback
import re
import sys


rgx = re.compile(r'\{\{%(.*)%\}\}')

def macrosub(txt, macros):

    macros = str(macros).strip()
    exec(macros)

    try:
        arr = [eval(a.strip()) for a in rgx.findall(txt)]
        gen = (y for y in arr)
        replacer = lambda m: next(gen)
        
        txt = rgx.sub(replacer, txt)
    except Exception as e:
        print("Error:", e, "\n", traceback.format_exc(), file=sys.stderr)
    
    return txt