#!/usr/bin/python

import os
from shlex import split
from glob import glob
from shutil import copy2
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE


def mk(ss, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
'''
subj_dict = {
    'LSRS': {
    'mprage1': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/3_t1_mprage_CNR_pat2',
    'mprage2': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201405271250/LNIF_Hasson_Uri_Eight-channel-RF-coil/36_t1_mprage_SNR_pat2'
    }}
'''
'''
Below is the second session anatomy
'''
subj_dict = {
    'LSRS': {
    'mprage_2ndsess': '/mnt/lnif-storage/urihas/MAdecorproj/HASURI002X49/19870826LSRS_201406031250/LNIF_Hasson_Uri_Eight-channel-RF-coil/4_t1_mprage_CNR_pat2'
    }}

for ss in subj_dict.keys():
    sess_dir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s' % locals ()
    for t1 in subj_dict[ss]:
        tmp_dir = '/mnt/lnif-storage/urihas/MAdecorproj/%(ss)s/dicomtmp%(t1)s' % locals()
        mk(ss, tmp_dir)
        for filename in glob(subj_dict[ss][t1]+'/*.DCM'):
            copy2(filename, tmp_dir)

        print os.getcwd()
        f = open('%(sess_dir)s/stdout_files/stdout_from_to3d_%(t1)s.txt' % locals (), 'w')
        cmd = 'Dimon -infile_prefix %(tmp_dir)s/*.DCM -dicom_org -gert_create_dataset -gert_outdir %(sess_dir)s -gert_to3d_prefix %(ss)s.%(t1)s.gert_reco' % locals()
        cmdargs = split(cmd)
        print cmdargs
        Popen(cmdargs, stdout = f, stderr = STDOUT)
        f.close()


