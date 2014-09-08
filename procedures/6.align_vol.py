#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def align_epis(ss):
    f = open('stdout_files/stdout_from_align_vol.txt', 'w')
    cmdargs = split('align_epi_anat.py -anat %(ss)s.mprage2.gert_reco.anat/T1_biascorr_brain.nii.gz -anat_has_skull no \
                    -epi %(ss)s_sess1_meanepi+orig -epi_base 0 -anat2epi -big_move' % locals())
#    cmdargs = split('align_epi_anat.py -anat LSRS.mprage2.gert_reco+orig -epi %(ss)s_sess1_avgepi+orig \
#                    -epi_base 0 -anat2epi -big_move -suffix _al2' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


subj_list = ['LSRS']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        align_epis(ss)

