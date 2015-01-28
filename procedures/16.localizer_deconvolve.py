#!/usr/bin/python
'''
Seeing if the localizer works
'''

from shlex import split
from subprocess import call
from subprocess import STDOUT
import os

def deconvolve(ss, model):
    '''leaving this out
    -censor %(ss)s.localizer.6mmblur.results/censor_%(ss)s.localizer.6mmblur_combined_2.1D \
    '''
    f = open('stdout_files/stdout_from_deconvolve.txt', 'w')
    cmdargs = split("3dDeconvolve -input errts.%(ss)s.localizer.6mmblur_REML+orig \
                    -polort A -num_stimts 4 \
                    -stim_times 1 stim_timing/onlyA.%(ss)s.txt %(model)s(21,1) -stim_label 1 onlyA \
                    -stim_times 2 stim_timing/onlyV.%(ss)s.txt %(model)s(21,1) -stim_label 2 onlyV \
                    -stim_times 3 stim_timing/AATTN.%(ss)s.txt %(model)s(21,1) -stim_label 3 AATTN \
                    -stim_times 4 stim_timing/VATTN.%(ss)s.txt %(model)s(21,1) -stim_label 4 VATTN \
                    -stim_times_subtract 21 \
                    -num_glt 13 \
                    -gltsym 'SYM: +onlyA' -glt_label 1 onlyAcontr \
                    -gltsym 'SYM: +onlyV' -glt_label 2 onlyVcontr \
                    -gltsym 'SYM: +AATTN' -glt_label 3 AATTNcontr \
                    -gltsym 'SYM: +VATTN' -glt_label 4 VATTNcontr \
                    -gltsym 'SYM: +onlyA -onlyV' -glt_label 5 onlyAvsonlyV \
                    -gltsym 'SYM: +onlyA -onlyV -AATTN -VATTN' -glt_label 6 onlyAvsALL \
                    -gltsym 'SYM: -onlyA +onlyV -AATTN -VATTN' -glt_label 7 onlyVvsALL \
                    -gltsym 'SYM: -onlyA -onlyV +AATTN -VATTN' -glt_label 8 AATTNvsALL \
                    -gltsym 'SYM: -onlyA -onlyV -AATTN +VATTN' -glt_label 9 VATTNvsALL \
                    -gltsym 'SYM: +onlyA -onlyV +AATTN -VATTN' -glt_label 10 AvsVcontr \
                    -gltsym 'SYM: -onlyA -onlyV +AATTN +VATTN' -glt_label 11 ATTNboth \
                    -gltsym 'SYM: -onlyA +AATTN' -glt_label 12 AATTNvsonlyA \
                    -gltsym 'SYM: -onlyV +VATTN' -glt_label 13 VATTNvsonlyV \
                    -fout -tout -x1D decon_nocensor.xmat.%(model)s.%(ss)s.1D \
                    -errts decon_nocensor.err.%(model)s.%(ss)s \
                    -bucket decon_nocensor.stats.%(model)s.%(ss)s " % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def testdecon(ss, bl):
    f = open('test_decon%s_stdout.txt' % bl, 'w')
    '''
    Includes removal of 21 sec (what was splaced at beginning of run to stabilize
    '''
    cmdargs = split("3dDeconvolve -nodata 392 1.5 -polort -1 -num_stimts 4 \
                    -stim_times 1 stim_timing/onlyA.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 2 stim_timing/onlyV.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 3 stim_timing/AATTN.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times 4 stim_timing/VATTN.%(ss)s.txt '%(bl)s(21)' \
                    -stim_times_subtract 21 \
                    -x1D %(ss)s.%(bl)s.xmat.1D " % locals())
    call(cmdargs, stdout = f, stderr = STDOUT)
    f.close()

def plot1d(fname, ss, bl):
    f = open('1dplot_stdout.txt', 'w')
    cmdargs = split('1dplot -one -thick -xlabel TIME -ynames onlyA onlyV AATTN VATTN \
                    -png %(fname)s %(ss)s.%(bl)s.xmat.1D' % locals())
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()

subj_list = ['CRSA']

if __name__ == "__main__":
    for ss in subj_list:
        os.chdir(os.environ['decor']+'/localizers/%s' % ss)   # adjusted for localizer
        for mm in ['BLOCK']:
            deconvolve(ss, mm)
        #for bltype in ['MION']:
        #    testdecon(ss, bltype)
        #    plot1d('test1.%s' % bltype, ss, bltype)
