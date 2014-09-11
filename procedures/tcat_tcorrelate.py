#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def tcat(ss, pref, epi_list):
    f = open('stdout_files/stdout_from_tcat.txt', 'w')
    cmdargs = split('3dTcat -prefix %(pref)s %(epi_list)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


def tcorr(ss, epi_cat1, epi_cat2):
    f = open('stdout_files/stdout_from_tcorrelate.txt', 'w')
    cmdargs = split('3dTcorrelate -prefix corr_out_AV_%(ss)s %(epi_cat1)s %(epi_cat2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()





stim_dict = {'LSRS': {'AV.1': ['AV1.1', 'AV2.1', 'AV3.1'], 'AV.2': ['AV1.2', 'AV2.2', 'AV3.2']}}

if __name__ == "__main__":
    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for rr in stim_dict[ss]:
            epi_list = ' '.join(map(str, ['errts.%(ss)s.%(st)s_REML_al+orig' % locals() for st in stim_dict[ss][rr]]))
            pref = '%(rr)s_%(ss)s_Tcat' % locals()
            #tcat(ss, pref, epi_list)
        
        epi1 = 'AV.1_%(ss)s_Tcat+orig.' % locals()
        epi2 = 'AV.2_%(ss)s_Tcat+orig.' % locals()
        tcorr(ss, epi1, epi2)
