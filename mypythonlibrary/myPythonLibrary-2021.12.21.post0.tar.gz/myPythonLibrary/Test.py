#coding=utf8

########################################################################
###                                                                  ###
### Created by Martin Genet, 2012-2022                               ###
###                                                                  ###
### University of California at San Francisco (UCSF), USA            ###
### Swiss Federal Institute of Technology (ETH), Zurich, Switzerland ###
### École Polytechnique, Palaiseau, France                           ###
###                                                                  ###
########################################################################

import filecmp
import numpy
import os
import sys
import shutil

########################################################################

class Test():
    
    def __init__(self,
        res_folder,
        perform_tests=1,
        stop_at_failure=1,
        clean_after_tests=1,
        ref_suffix="-ref",
        qois_suffix="-qois",
        qois_ext=".dat"):

        self.res_folder        = res_folder
        self.perform_tests     = perform_tests
        self.stop_at_failure   = stop_at_failure
        self.clean_after_tests = clean_after_tests
        self.ref_suffix        = ref_suffix
        self.qois_suffix       = qois_suffix
        self.qois_ext          = qois_ext
        self.success           = True

        shutil.rmtree(self.res_folder, ignore_errors=1)
        os.mkdir(self.res_folder)

    def __del__(self):
        if (self.clean_after_tests) and (self.success):
            shutil.rmtree(self.res_folder, ignore_errors=1)

    def test(self, res_basename):
        if (self.perform_tests):
            res_filename = self.res_folder                +"/"+res_basename+self.qois_suffix+self.qois_ext
            ref_filename = self.res_folder+self.ref_suffix+"/"+res_basename+self.qois_suffix+self.qois_ext
            self.success = self.filecmp(res_filename, ref_filename)
            if not (self.success):
                print ("Result in "+res_filename+" (\n"+open(res_filename).read()+") "+\
                       "does not correspond to "+\
                       "reference in "+ref_filename+" (\n"+open(ref_filename).read()+").")
                if (self.stop_at_failure):
                    print ("Aborting.")
                    sys.exit(1)

    def filecmp(self, res_filename, ref_filename):
        return filecmp.cmp(res_filename, ref_filename)
