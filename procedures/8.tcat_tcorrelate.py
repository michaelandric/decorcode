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
    cmdargs = split('3dTcorrelate -polort -1 -prefix %(pref)s %(epi_cat1)s %(epi_cat2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()


def meanRes(pref, epi1, epi2):
    f = open('stdout_files/stdout_from_3dmean.txt', 'w')
    cmdargs = split('3dMean -prefix %(pref)s %(epi1)s %(epi2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close() 




subj_list = ['LSRS']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())

        f = open(os.environ['decor']+'/decorcode/stim_timing_info/Timing_layout.txt', 'r')
        run = []
        clip = []
        tt = []
        for line in f:
            i, j, k = line.split()
            run.append(i)
            clip.append(j)
            tt.append(k)

        segments = set(c.split('_')[0] for c in clip)
        for seg in segments:
            '''This is for the AV correlations'''
            epi1 = '%(seg)s_AV.1_%(ss)s_spliced+orig' % locals()
            epi2 = '%(seg)s_AV.2_%(ss)s_spliced+orig' % locals()
            pref = '%(seg)s_AV_%(ss)s_tcorrout' % locals()
            tcorr(pref, epi1, epi2)

            '''This is to get low level visual and auditory correlations'''
            epi1 = '%(seg)s_V_%(ss)s_spliced+orig' % locals()
            epi2 = '%(seg)s_A_%(ss)s_spliced+orig' % locals()
            pref = '%(seg)s_lowlev_%(ss)s_tcorrout' % locals()
            tcorr(pref, epi1, epi2)

            for m in ('V', 'A'):
                '''These are for the V vs AV, A vs AV correlations'''
                for i in xrange(1,3):
                    epi1 = '%(seg)s_%(m)s_%(ss)s_spliced+orig' % locals()
                    epi2 = '%(seg)s_AV.%(i)d_%(ss)s_spliced+orig.' % locals()
                    pref = '%(seg)s_%(m)s.%(i)d_%(ss)s_tcorrout' % locals()
                    tcorr(pref, epi1, epi2)

                epi1 = '%(seg)s_%(m)s.1_%(ss)s_tcorrout+orig' % locals()
                epi2 = '%(seg)s_%(m)s.2_%(ss)s_tcorrout+orig' % locals()
                pref = '%(seg)s_%(m)s_%(ss)s_tcorrout+orig' % locals()
                meanRes(pref, epi1, epi2)


