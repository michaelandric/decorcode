#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

def qwarp(ss, pref):
    f = open('stdout_files/stdout_from_qwarp.txt', 'w')
    cmdargs = split('3dQwarp -prefix %(pref)s -allineate -useweight -duplo -base %(ss)s_sess1_meanepi+orig -source %(ss)s_sess2_meanepi+orig' % locals())
    '''Ran this AFTER allineate via align_epi_anat.py with '-giant_move'. But that resamples to 4 x 4 x 4, thus this uses 'resample' options.
    3dQwarp -verb -prefix NNPT_sess2_meanepi_Q -duplo -useweight -base NNPT_sess1_meanepi+orig. -source NNPT_sess2_meanepi_gm+orig. -resample'''
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def nwarpapply(ss, pref):
    f = open("stdout_files/stdout_from_nwarpapply.txt", "w")
    cmdargs = split("3dNwarpApply -nwarp LSRS_sess2_meanepi_Q2_WARP+orig -master NWARP \
                    -affter LSRS_sess2_meanepi_Q2_Allin.aff12.1D -source %(ss)s.AV3.2.results/pb03.%(ss)s.AV3.2.r01.volreg+orig \
                    -prefix %(pref)s" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

if __name__ == "__main__":

    for ss in ['LSRS']:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        #pref = '%(ss)s_sess2_meanepi_Q2' % locals()
        #qwarp(ss, pref)
        pref = '%(ss)s_AV3.2_QWrp' % locals()
        nwarpapply(ss, pref)



