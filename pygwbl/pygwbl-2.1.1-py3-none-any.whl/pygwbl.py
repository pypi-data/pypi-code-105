import os

__all__=["svg2emf","about"]


def svg2emf(FileName):
    os.system("inkscape --export-type=emf "+ FileName)

def about():
    print("Hi, I am Dagwbl. ")

if __name__=="__main__":
    print('pygwbl: running by myself')
else:
    print('pygwbl: I am being imported from other module')
