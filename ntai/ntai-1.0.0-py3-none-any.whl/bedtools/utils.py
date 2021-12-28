def bed_str_to_list(bed:list):
    '''Separetes a multiline TSV into a list of list for each line'''
    return [line.split('\t') for line in bed.rstrip('\n').split('\n')]

def bed_list_to_str(bed:str):
    '''Concatenates a list of lists into TSV format'''
    return '\n'.join(['\t'.join([str(el) for el in sub]) for sub in bed])
