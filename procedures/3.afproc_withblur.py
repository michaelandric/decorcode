# -*- coding: utf-8 -*-
"""
code overhaul on Fri May  6 10:23:57 2016

@author: andric
"""

import os
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import STDOUT


def afniproc(subj, runid, subjid, volregbase):
    """This sets up an afni_proc.py script"""
    print('Now generating afni_proc...')
    call('afni_proc.py -subj_id {} -dsets {}.{}.TRIM+orig \
                    -blocks despike tshift volreg blur mask regress \
                    -volreg_base_dset {}.{}.TRIM+orig \
                    -blur_size 6 \
                    -regress_use_tproject no \
                    -regress_censor_motion 0.3 \
                    -regress_censor_outliers 0.1 \
                    -regress_apply_mot_types demean deriv \
                    -regress_run_clustsim no \
                    -regress_reml_exec'.format(subjid, runid, subj,
                                               volregbase, subj), shell=True)


def run_afniproc(subjid):
    """This executes the tcsh afni_proc script"""
    runcmd = split('tcsh -xef proc.{}'.format(subjid))
    stdf = open('output.proc.{}'.format(subjid), 'w')
    print('Now running afni_proc \n')
    Popen(runcmd, stdout=stdf, stderr=STDOUT)
    stdf.close()
    print('Check progress yourself... \n')


if __name__ == "__main__":

    STIMDICT = {
        'LNSE': {'SC5': ['SC5', 'SC2', 'SC6', 'AV3.1', 'AV2.1', 'AV1.1'],
                 'SC1': ['SC1', 'SC4', 'SC3', 'AV1.2', 'AV3.2', 'AV2.2'],
                 'Rest': ['Rest']}}

    for subject in STIMDICT.keys():
        print('setting work dir: ')
        os.chdir(os.environ['decor']+'/localizers/%s' % subject)
        for ref in STIMDICT[subject]:
            for runident in STIMDICT[subject][ref]:
                subjrun = '{}.{}.6mmblur'.format(subject, runident)
                afniproc(subject, runident, subjrun, ref)
                run_afniproc(subjrun)   # this is separate
