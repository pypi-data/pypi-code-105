import scipy.io as sio
from obspy import read
import os, sys
import argparse



info_string = '''
Python utility program to convert mseed file to mat (by Utpal Kumar)
'''

PARSER = argparse.ArgumentParser(description=info_string)

def convertmseed2mat(mseedfile, output_mat=None):
    
    st = read(mseedfile)

    filename, _ = os.path.splitext(mseedfile)
    if output_mat is None:
        outfilename = filename +".mat"
    else:
        outfilename = output_mat

    outdict = {}
    
    outdict['stats'] = {}
    outdict['data'] = {}
    
    for ii,tr in enumerate(st):
        outdict['stats'][f'stats_{ii}'] = {}
        for val in tr.stats:
            if val in ['starttime', 'endtime']:
                outdict['stats'][f'stats_{ii}'][val] = str(tr.stats[val])
            else:
                outdict['stats'][f'stats_{ii}'][val] = tr.stats[val]
        outdict['data'][f"data_{ii}"] = tr.data
    
        
    sio.savemat(
        outfilename, outdict
    )
    sys.stdout.write(f"Output file: {outfilename}\n")

if __name__ == '__main__':
    PARSER.add_argument("-inp",'--input_mseed', type=str, help="input mseed file, e.g. example_2020-05-01_IN.RAGD..BHZ.mseed", required=True)
    PARSER.add_argument("-out",'--output_mat', type=str, help="output mat file name, e.g. example_2020-05-01_IN.RAGD..BHZ.mat")
    

    args = PARSER.parse_args()
    mseedfile = args.input_mseed
    output_mat = args.output_mat
    convertmseed2mat(mseedfile, output_mat)