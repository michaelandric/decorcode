# -*- coding: utf-8 -*-
"""
Code overhaul on Fri May  6 10:23:57 2016.

Added setlog funciton June 8 2016
@author: andric
"""

import os
import pandas as pd
from shlex import split
from setlog import setup_log
from subprocess import Popen
from subprocess import call
from subprocess import STDOUT
from subprocess import PIPE


def afniproc(subj, runid, subjid, volregbase):
    """Set up an afni_proc.py script."""
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


def run_afniproc(log, subjid):
    """Execute the tcsh afni_proc script."""
    log.info('Doing run_afniproc.')
    runcmd = split('tcsh -xef proc.{}'.format(subjid))
    print('Now running afni_proc \n')
    proc = Popen(runcmd, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())
    print('Check progress yourself... \n')


def build_subject_dict(subjectlist):
    """Build dictionary of subject and run orders."""
    orderfile = os.path.join(os.environ['decor'],
                             'SS_runs_presentation_orders_and_answers.csv')
    df = pd.read_csv(orderfile)
    stimdict = {}
    for subj in subjectlist:
        seriesorder = pd.Series(df.loc[df.SSname == subj, 'stim_name'])
        subidx = list(seriesorder.iloc[[0, 6]])
        subjitem = {subj: {subidx[0]: list(seriesorder.iloc[:6]),
                    subidx[1]: list(seriesorder.iloc[6:]), 'Rest': ['Rest']}}
        stimdict.update(subjitem)

    return stimdict


if __name__ == '__main__':

    SUBJECTLIST = ['PMBI']
    STIMDICT = build_subject_dict(SUBJECTLIST)

    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                        'afproc_withblur'))
    logfile.info('started 3.afproc_withblur.py')

    for subject in SUBJECTLIST:
        print('setting work dir: ')
        os.chdir(os.path.join(os.environ['decor'], subject))
        print(os.getcwd())
        for ref in STIMDICT[subject]:
            for runident in STIMDICT[subject][ref]:
                subjrun = '{}.{}.6mmblur'.format(subject, runident)
                afniproc(subject, runident, subjrun, ref)
                run_afniproc(logfile, subjrun)   # this is separate
