import os
import demo1


__all__=["svg2emf","about","m3u8_download"]
# __version__=666

def m3u8_download(url,filename=None):
    cmd = "N_m3u8DL-CLI.exe"
    os.system(cmd)

def svg2emf(FileName):
    os.system("inkscape --export-type=emf "+ FileName)

def about():
    print("Hi, I am Dagwbl. ")
    return True

if __name__=="__main__":
    print('pygwbl: running by myself')
else:
    print('pygwbl: I am being imported from other module')
