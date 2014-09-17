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


def tcorr(pref, epi_cat1, epi_cat2):
    f = open('stdout_files/stdout_from_tcorrelate.txt', 'w')
    cmdargs = split('3dTcorrelate -prefix %(pref)s %(epi_cat1)s %(epi_cat2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


def meanRes(pref, epi1, epi2):
    f = open('stdout_files/stdout_from_3dmean.txt', 'w')
    cmdargs = split('3dMean -prefix %(pref)s %(epi1)s %(epi2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close() 




#stim_dict = {'LSRS': {'AV.1': ['AV1.1', 'AV2.1', 'AV3.1'], 'AV.2': ['AV1.2', 'AV2.2', 'AV3.2']}}
subj_list = ['SSGO']
modals = ['AV', 'V', 'A']


if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        '''
        for rr in stim_dict[ss]:
            epi_list = ' '.join(map(str, ['errts.%(ss)s.%(st)s_REML_al+orig' % locals() for st in stim_dict[ss][rr]]))
            pref = '%(rr)s_%(ss)s_Tcat' % locals()
            #tcat(ss, pref, epi_list)
        
        epi1 = 'AV.1_%(ss)s_Tcat+orig.' % locals()
        epi2 = 'AV.2_%(ss)s_Tcat+orig.' % locals()
        tcorr(ss, epi1, epi2)
        '''
        
        for m in modals:
            if m == 'AV':
                epi1 = 'AV.1_%(ss)s_tcat+orig.' % locals()
                epi2 = 'AV.2_%(ss)s_tcat+orig.' % locals()
                pref = 'AV_%(ss)s_tcorrout' % locals()
                tcorr(pref, epi1, epi2)
            else:
                for i in xrange(1,3):
                    epi1 = '%(m)s_%(ss)s_tcat+orig.' % locals()
                    epi2 = 'AV.%(i)d_%(ss)s_tcat+orig.' % locals()
                    pref = '%(m)s.%(i)d_%(ss)s_tcorrout' % locals()
                    tcorr(pref, epi1, epi2)

                epi1 = '%(m)s.1_%(ss)s_tcorrout+orig' % locals()
                epi2 = '%(m)s.2_%(ss)s_tcorrout+orig' % locals()
                pref = '%(m)s_%(ss)s_tcorrout+orig' % locals()
                meanRes(pref, epi1, epi2)



