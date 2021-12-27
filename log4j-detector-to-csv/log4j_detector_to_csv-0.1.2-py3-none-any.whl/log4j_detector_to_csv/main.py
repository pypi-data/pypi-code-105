import json
import glob
import os
import csv
import argparse

def process_file(input,output):
    detection_liste = []

    for file in glob.iglob(input):
        with open(file) as data_file:
            try:
                hits = json.load(data_file)['hits']
                for hit in hits:
                    typ = ""
                    filename = ""
                    
                    if '_OLD_' in hit:
                        typ = '_OLD_'
                        filename = hit.get('_OLD_')
                        
                    if '_OKAY_' in hit:
                        typ = '_OKAY_'
                        filename = hit.get('_OKAY_')
                        
                    if '_SAFE_' in hit:
                        typ = '_SAFE_'
                        filename = hit.get('_SAFE_')
                        
                    if '_POTENTIALLY_SAFE_' in hit:
                        typ = '_POTENTIALLY_SAFE_'
                        filename = hit.get('_POTENTIALLY_SAFE_')
                        
                    if '_VULNERABLE_' in hit:
                        typ = '_VULNERABLE_'
                        filename = hit.get('_VULNERABLE_')
                        
                    if '_THE_END_' in hit:
                        continue
                    
                    detection_liste.append([
                        os.path.basename(file).split(".")[0],
                        typ,
                        filename
                    ])
                
            except ValueError as e:
                print(f'Error in processing file {file} : {e}')
                pass


    with open(output, 'w') as output:
        wr = csv.writer(output)
        wr.writerow(["host","type","filename"])
        wr.writerows(detection_liste)

def main():
    try:
        parser = argparse.ArgumentParser(description='Convert log4j-detector json file into one csv')
        parser.add_argument('-i', '--input', dest="input", help='Input directory', required=True)
        parser.add_argument('-o', '--output', dest="output", help='Output directory', required=True)
        args = parser.parse_args()
        process_file(args.input+"/*.json", args.output)
    except Exception as e:
        print(e)
