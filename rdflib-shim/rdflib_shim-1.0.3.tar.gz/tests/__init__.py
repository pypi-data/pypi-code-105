import os.path

CWD = os.path.dirname(__file__)
OUTDIR = os.path.join(CWD, 'output')
os.makedirs(OUTDIR, exist_ok=True)