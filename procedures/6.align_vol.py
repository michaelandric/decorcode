#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


def align_epis(ss, t1):
    f = open('stdout_files/stdout_from_align_vol.txt', 'w')
    #cmdargs = split('align_epi_anat.py -anat %(ss)s.%(t1)s.gert_reco.anat/T1_biascorr_brain.nii.gz -anat_has_skull no \
    #                -epi %(ss)s_sess1_meanepi+orig -epi_base 0 -suffix _%(t1)s -anat2epi -big_move' % locals())
    '''below cmd is for localizer test'''
    cmdargs = split('align_epi_anat.py -anat %(ss)s.%(t1)s.gert_reco.anat/T1_biascorr_brain.nii.gz -anat_has_skull no \
                    -epi mean.localizer.%(ss)s.TRIM+orig -epi_strip 3dAutomask -epi_base 0 \
                    -suffix _%(t1)s -anat2epi -big_move' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['IAGO']
#t1_list = ['mprage1', 'mprage2', 'mprage_2ndsess']
t1_list = ['mprage1']

if __name__ == "__main__":
    for ss in subj_list:
        for t1 in t1_list:
            os.chdir(os.environ['decor']+'/localizers/%s' % ss)   # adjusted for localizer
            align_epis(ss, t1)

