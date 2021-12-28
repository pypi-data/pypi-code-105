import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path,"libs"))

import BIMM

def bimm_from_path(str,dict_path=""):
    if dict_path=="":
        dict_path=current_path+"/data/30wChinesesSeqDic_clean.txt"
    return BIMM.bimm_from_path(str,dict_path)

def fmm(str,words_dict):
    return BIMM.fmm(str,words_dict)

def bimm(str,words_dict):
    return BIMM.bimm(str,words_dict)

def bmm(str,words_dict):
    return BIMM.bmm(str,words_dict)

def read_dict(dict_path):
    return BIMM.read_dict(dict_path)