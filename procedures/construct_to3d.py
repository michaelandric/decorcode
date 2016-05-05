# -*- coding: utf-8 -*-
"""
re-working this Thu May  5 12:04:12 2016

@author: andric

Run names, e.g., 'SC5' correspond to the 
stimuli file (SC5.avi in this case) that were shown.
Order of these stimuli files found in 
Google Drive file 'SS runs; presentation order and answers'
"""


import os
import shutil
from shlex import split
from glob import glob
from subprocess import Popen
from subprocess import STDOUT


class DoReconstruction:

    def __init__(self, subject, scan_dictionary):
        self.ss = subject
        self.scan_dict = scan_dictionary

    def mk(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
    
    def rmdir(self, dir):
        shutil.rmtree(dir)
    
    def reconstruct(self):
        dicom_base = os.path.join(os.environ['decor'],
                                  'subject_dicoms/HASURI002X49')
        subj_dir = os.path.join(os.environ['decor'], self.ss)
        os.chdir(subj_dir)
        print("Now in: \n")
        print(os.getcwd())

        self.mk(os.path.join(subj_dir, 'stdout_files'))
        for session_dir in self.scan_dict:
            for stim, i in self.scan_dict[session_dir]:
                tmp_dir = os.path.join(subj_dir, 'dicomtmp{}'.format(stim))
                self.mk(tmp_dir)

                dic_dir = os.path.join(dicom_base, session_dir,
                                       'LNIF_Hasson_Uri_Eight-channel-RF-coil',
                                       '{}_lnif_epi1_4x4x4_TR1500_DiCo'.format(i))
                for filename in glob('{}/*.DCM'.format(dic_dir)):
                    shutil.copy2(filename, tmp_dir)
                
                f = open('stdout_files/stdout_from_to3d_{}.txt'.format(stim), 'w')
                cmdargs = split('Dimon -infile_prefix {}/*.DCM -dicom_org \
                                -gert_create_dataset -gert_outdir {} \
                                -gert_to3d_prefix raw.{}.{}.gert_reco'.format(
                                tmp_dir, subj_dir, self.ss, stim))
                print(cmdargs)
                Popen(cmdargs, stdout=f, stderr=STDOUT)
                f.close()


def main():

    scan_dict = {'19840308LNSE_201408251340':
        [('SC5', 13), ('SC2', 17), ('SC6', 21),
         ('AV3.1', 25), ('AV2.1', 29), ('AV1.1', 33), ('Rest', 9)],
                 '19840308LNSE_201411031400':
                     [('SC1', 7), ('SC4', 11), ('SC3', 15),
                      ('AV1.2', 19), ('AV3.2', 23), ('AV2.2', 27)]}
    dr = DoReconstruction('LNSE', scan_dict)
    dr.reconstruct()

if __name__ == '__main__':
    main()