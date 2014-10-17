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



subj_list = ['JNWL']

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
        os.chdir(os.environ['decor']+'/%(ss)s/6mmblur_results' % locals())
        for i, cc in enumerate(clip):
            if 'AV' in run[i]:
                for x in xrange(1,3):
                    pref = '%s.%d_%s_splicy' % (cc, x, ss)
                    '''Here adding 7 and 3 TRs (10.5 and 4.5 s) to beginning and end'''
                    a,b = map(int, tt[i].split(":"))
                    a = a + 7
                    b = b + 3
                    startstop = '%s..%s' % (a, b)
                    epi = 'errts.%s.%s.%d.6mmblur_REML_gm+orig[%s]' % (ss, run[i], x, startstop)
                    splice(ss, pref, epi)

            pref = '%s_%s_splicy' % (cc, ss)
            a,b = map(int, tt[i].split(":"))
            a = a + 7
            b = b + 3
            startstop = '%s..%s' % (a, b)
            epi = 'errts.%s.%s.6mmblur_REML_gm+orig[%s]' % (ss, run[i], startstop)
            splice(ss, pref, epi)


