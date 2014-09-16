#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def align_epis(ss, t1):
    f = open('stdout_files/stdout_from_align_vol.txt', 'w')
    #cmdargs = split('align_epi_anat.py -anat %(ss)s.%(t1)s.gert_reco.anat/T1_biascorr_brain.nii.gz -anat_has_skull no \
    cmdargs = split('align_epi_anat.py -anat T1_biascorr_brain.nii.gz -anat_has_skull no \
                    -epi %(ss)s_sess1_meanepi+orig -epi_base 0 -suffix _%(t1)s -anat2epi -big_move' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['SSGO']
#t1_list = ['mprage1', 'mprage2', 'mprage_2ndsess']
t1_list = ['mprage1']

if __name__ == "__main__":
    for ss in subj_list:
        for t1 in t1_list:
            os.chdir(os.environ['decor']+'/%(ss)s' % locals())
            align_epis(ss, t1)

