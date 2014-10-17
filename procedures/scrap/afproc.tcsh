#!/bin/tcsh


afni_proc.py -subj_id LSRS \
    -dsets SC5.LSRS.TRIM+orig \
    -blocks despike tshift volreg blur mask regress \
    -volreg_base_dset SC5.LSRS.TRIM+orig \
    -regress_censor_motion 0.3 \
    -regress_censor_outliers 0.1 \
    -regress_apply_mot_types demean deriv \
    -regress_run_clustsim no \
    -regress_est_blur_errts   

tcsh -xef proc.LSRS |& tee output.proc.LSRS
