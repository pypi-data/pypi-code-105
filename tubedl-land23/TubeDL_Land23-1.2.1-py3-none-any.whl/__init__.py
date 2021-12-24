from TubeDL import tube
import sys
import os
from time import sleep 
def Setup():
    args = []
    #if (sys.argv[0] == os.path.basename(__file__)):
    #    args = sys.argv[1:]
    #else:
    #    args = sys.argv
    args = sys.argv[1:]
    if (len(args) == 0):
        tube.ShowHelp()
        tube.Close()

    tube.Main(args)
