#!/usr/bin/python

import os
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

def afniproc(ss, runID, epi_list, volregbase):
    call("afni_proc.py -subj_id %(ss)s.%(runID)s -out_dir %(ss)s_AV.1 -dsets %(epi_list)s \
                    -blocks despike tshift volreg mask regress \
                    -volreg_base_dset %(volregbase)s.%(ss)s.TRIM+orig \
                    -regress_censor_motion 0.3 \
                    -regress_censor_outliers 0.1 \
                    -regress_basis 'dmBLOCK' \
                    -regress_stim_times /mnt/lnif-storage/urihas/MAdecorproj/decorcode/stim_timing_info/AV_all3runs.1D \
                    -regress_stim_types AM1 \
                    -regress_stim_labels AV \
                    -regress_apply_mot_types demean deriv \
                    -regress_run_clustsim no \
                    -regress_reml_exec \
                    -regress_est_blur_errts" % locals(), shell = True)
                   

stim_dict = {'LSRS': {'AV': ['AV1.1', 'AV2.1', 'AV3.1']}}


if __name__ == "__main__":

    for ss in stim_dict.keys():
        os.chdir(os.environ['decor']+'/%(ss)s' % locals())
        for rr in stim_dict[ss]:
            epi_list = ' '.join(map(str, ['%(st)s.%(ss)s.TRIM+orig' % locals() for st in stim_dict[ss][rr]]))
            afniproc(ss, rr, epi_list, 'SC5')
            runcmd = split('tcsh -xef proc.%(ss)s.%(rr)s' % locals())
            f = open('output.proc.%(ss)s.%(rr)s' % locals(), 'w')
            Popen(runcmd, stdout = f, stderr = STDOUT)
            f.close()

