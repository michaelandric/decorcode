#!/usr/bin/python

import os
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT

def afniproc(ss, runID, subj_id, volregbase):
    print 'Now generating afni_proc...'
    call('afni_proc.py -subj_id %(subj_id)s -dsets %(runID)s.%(ss)s.TRIM+orig \
                    -blocks despike tshift volreg blur mask regress \
                    -volreg_base_dset %(volregbase)s.%(ss)s.TRIM+orig \
                    -blur_size 6 \
                    -regress_use_tproject no \
                    -regress_censor_motion 0.3 \
                    -regress_censor_outliers 0.1 \
                    -regress_apply_mot_types demean deriv \
                    -regress_run_clustsim no \
                    -regress_reml_exec' % locals(), shell = True)


stim_dict = {
    'CRSA': {'localizer': ['localizer']}
    }

if __name__ == "__main__":
    for ss in stim_dict.keys():
        print 'setting work dir: '
        print os.chdir(os.environ['decor']+'/localizers/%s' % ss)   # set to do localizer
        for ref in stim_dict[ss]:
            for rr in stim_dict[ss][ref]:
                subjid = '%s.%s.6mmblur' % (ss, rr)   # NOTE HERE 'subjid' IS COMBO OF SS, RR, AND SMOOTHING 
                afniproc(ss, rr, subjid, ref)
                runcmd = split('tcsh -xef proc.%s' % subjid)
                f = open('output.proc.%s' % subjid, 'w')
                print 'Now running afni_proc'
                Popen(runcmd, stdout = f, stderr = STDOUT)
                f.close()
                print 'All done!'
