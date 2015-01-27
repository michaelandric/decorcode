#!/usr/bin/python
'''
Seeing if the localizer works
'''

from shlex import split
from subprocess import call
from subprocess import STDOUT
import os

def deconvolve(ss):
    f = open('stdout_files/stdout_from_deconvolve.txt', 'w')
    cmdargs = split('3dDeconvolve -input errts.%(ss)s.localizer.6mmblur_REML+orig \
                    -censor %(ss)s.localizer.6mmblur.results/censor_%(ss)s.localizer.6mmblur_combined_2.1D \
                    -polort A -num_stimts 4 \
                    -stim_times 1 onlyA.%(ss)s.txt MIONN(21) \
                    -stim_times 2 onlyV.%(ss)s.txt MIONN(21) \
                    -stim_times 3 AATTN.%(ss)s.txt MIONN(21) \
                    -stim_times 4 VATTN.%(ss)s.txt MIONN(21) \
                    -fout -tout -x1D X.xmat.%(ss)s.1D \
                    -errts decon.err.%(ss)s \
                    -bucket decon.stats.%(ss)s ' % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def testdecon(bl, fname):
    f = open('test_decon_stdout.txt', 'w')
    '''
    Includes removal of 21 sec (what was splaced at beginning of run to stabilize
    '''
    cmdargs = split("3dDeconvolve -nodata -polort -1 -num_stimts 4 \
                    -stim_times 1 stim_timing/onlyA.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 2 stim_timing/onlyV.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 3 stim_timing/AATTN.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 4 stim_timing/VATTN.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times_subtract 21 \
                    -x1D stdout: \
                    | 1dplot -png %(fname)s -stdin -one -thick \
                    -xlabel TIME -ynames onlyA onlyV AATTN VATTN" % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

subj_list = ['CRSA']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/localizers/%s' % ss)   # adjusted for localizer
        #deconvolve(ss)
        for bltype in ['MIONN', 'WAV']:
            fname = 'test.%s' % bltype
            testdecon(bltype, fname)