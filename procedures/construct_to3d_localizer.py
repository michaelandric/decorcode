#!/usr/bin/python

import os
import shutil
from shlex import split
from glob import glob
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE

"""
For full provenance, will include full paths

This version is for the localizer stimuli. First collected Dec. 11 2014. 

"""

def mk(ss, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def rmdir(ss, dir):
    shutil.rmtree(dir)

stim_dict = {
    'IAGO': {
    'localizer': '/mnt/lnif-storage/urihas/MAdecorproj/IAGOlocalizer/23_lnif_epi1_4x4x4_TR1500_DiCo/'
    }}

for ss in stim_dict.keys():
    sess_dir = '/mnt/lnif-storage/urihas/MAdecorproj/localizers/%(ss)s' % locals ()
    os.chdir(sess_dir)

    for stim in stim_dict[ss]:
        tmp_dir = '/mnt/lnif-storage/urihas/MAdecorproj/localizers/%(ss)s/dicomtmp%(stim)s' % locals()
        mk(ss, tmp_dir)

        for filename in glob(stim_dict[ss][stim]+'/*.DCM'):
            shutil.copy2(filename, tmp_dir)

        f = open('stdout_files/stdout_from_to3d_'+stim+'.txt', 'w')
        cmdargs = split('Dimon -infile_prefix %(tmp_dir)s/*.DCM -dicom_org -gert_create_dataset -gert_outdir %(sess_dir)s -gert_to3d_prefix raw.%(ss)s.%(stim)s.gert_reco' % locals())
        print cmdargs
        Popen(cmdargs, stdout = f, stderr = STDOUT)
        f.close()


