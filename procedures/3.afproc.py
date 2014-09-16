#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

def afniproc(ss, runID, volregbase):
    call('afni_proc.py -subj_id %(ss)s.%(runID)s -dsets %(runID)s.%(ss)s.TRIM+orig \
                    -blocks despike tshift volreg blur mask regress \
                    -volreg_base_dset %(volregbase)s.%(ss)s.TRIM+orig \
                    -blur_size 6 \
                    -regress_censor_motion 0.3 \
                    -regress_censor_outliers 0.1 \
                    -regress_apply_mot_types demean deriv \
                    -regress_run_clustsim no \
                    -regress_reml_exec \
                    -regress_est_blur_errts' % locals(), shell = True)
                   

stim_dict = {
    #'LSRS': {'SC5': ['SC5', 'SC6', 'SC2', 'AV2.1', 'AV1.1', 'AV3.1'], 'SC1': ['SC1', 'SC3', 'SC4', 'AV1.2', 'AV3.2', 'AV2.2']}
    #'NNPT': {'SC1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'SC4': ['SC4', 'SC5', 'SC6', 'AV3.2', 'AV2.2', 'AV1.2'], 'Rest': ['Rest']}
    'SSGO': {'SC1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'SC4': ['SC4', 'SC5', 'SC6', 'AV3.2', 'AV2.2', 'AV1.2'], 'Rest': ['Rest']}
    #'SSGO': {'AV1.1': ['SC1', 'SC2', 'SC3', 'AV1.1', 'AV2.1', 'AV3.1'], 'AV3.2': ['SC4', 'SC5', 'SC6', 'AV3.2', 'AV2.2', 'AV1.2'], 'Rest': ['Rest']}
    #'NNPT': {'Rest': ['Rest']}
    }

if __name__ == "__main__":
    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for ref in stim_dict[ss]:
            for rr in stim_dict[ss][ref]:
                afniproc(ss, rr, ref)
                runcmd = split('tcsh -xef proc.%(ss)s.%(rr)s' % locals())
                f = open('output.proc.%(ss)s.%(rr)s' % locals(), 'w')
                Popen(runcmd, stdout = f, stderr = STDOUT)
                f.close()

