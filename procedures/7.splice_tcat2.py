#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def splice(ss, pref, epi):
    f = open('stdout_files/stdout_from_splice1.txt', 'w')
    cmdargs = split('3dTcat -prefix %(pref)s %(epi)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def tcat(ss, pref, epi_list):
    f = open('stdout_files/stdout_from_tcat.txt', 'w')
    cmdargs = split('3dTcat -prefix %(pref)s %(epi_list)s' % locals())
    try:
        call(cmdargs, stdout = f, stderr = STDOUT)
    except:
        'SOMETHING BROKE----------TCAT NOT WORKING'
    f.close()

def tcorr(ss, epi_cat1, epi_cat2):
    f = open('stdout_files/stdout_from_tcorrelate.txt', 'w')
    cmdargs = split('3dTcorrelate -prefix corr_out_AV_%(ss)s %(epi_cat1)s %(epi_cat2)s' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()



subj_list = ['SSGO']

if __name__ == "__main__":

    f = open(os.environ['decor']+'/decorcode/stim_timing_info/Timing_layout.txt', 'r')
    run = []
    clip = []
    tt = []
    for line in f:
        i, j, k = line.split()
        run.append(i)
        clip.append(j)
        tt.append(k)

    AV = [c for c in clip if c.split('_')[1] == 'AV']
    V = [c for c in clip if c.split('_')[1] == 'V']
    A = [c for c in clip if c.split('_')[1] == 'A']
    AV.sort()
    V.sort()
    A.sort()

    for ss in subj_list:
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for i, cc in enumerate(clip):
            if 'AV' in run[i]:
                for x in xrange(1,3):
                    pref = '%s.%d_%s_spliced' % (cc, x, ss)
                    a,b = tt[i].split(":")
                    startstop = '%s..%s' % (a, b)
                    epi = 'errts.%s.%s.%d_REML_al+orig[%s]' % (ss, run[i], x, startstop)
                    splice(ss, pref, epi)

            pref = '%s_%s_spliced' % (cc, ss)
            a,b = tt[i].split(":")
            startstop = '%s..%s' % (a, b)
            epi = 'errts.%s.%s_REML_al+orig[%s]' % (ss, run[i], startstop)
            splice(ss, pref, epi)

        for x in xrange(1, 3):        
            for m in ['AV']:
                epi_list = ' '.join(['%s.%d_%s_spliced+orig' % (c, x, ss) for c in eval(m)])
                pref = '%s.%d_%s_tcat' % (m, x, ss)
                tcat(ss, pref, epi_list)

        for m in ['V', 'A']:
            epi_list = ' '.join(['%s_%s_spliced+orig' % (c, ss) for c in eval(m)])
            pref = '%s_%s_tcat' % (m, ss)
            tcat(ss, pref, epi_list)


