# -*- coding: utf-8 -*-
"""
code overhaul on Fri May  6 13:27:13 2016.

See avgepis doc for warning about the way these should be run

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import STDOUT
from subprocess import PIPE
from setlog import setup_log
import pandas as pd


def avgepis(log, subj, sess, epilist):
    """Average the epis together.

    This must be done first before the other methods in this code!
    """
    log.info('Doing avgepis for %s %s', subj, sess)
    cmdargs = split('3dMean -prefix {}_{}_6mmblur_avgepi {}'.format(
        subj, sess, epilist))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def mean_sess(log, subj, sess):
    """Get the the mean over the runs."""
    log.info('Doing mean_sess for %s %s', subj, sess)
    cmdargs = split('3dTstat -prefix {}_{}_6mmblur_meanepi \
                    -mean {}_{}_6mmblur_avgepi+orig'.format(
                        subj, sess, subj, sess))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def align_epis(log, subj):
    """Creating template to align second session runs to first session."""
    log.info('Doing align_epis %s', subj)
    cmdargs = split('align_epi_anat.py -dset1 {}_sess1_6mmblur_meanepi+orig \
                    -dset2 {}_sess2_6mmblur_meanepi+orig -dset2to1 \
                    -epi_base 0 -anat_has_skull no -master_dset1_dxyz BASE \
                    -giant_move -suffix _gm'.format(subj, subj))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def allineate(log, subj, cond):
    """Align the datasets.

    Only need this for aligning second session runs to their
    first session counterparts. First session already good from 3dvolreg.
    """
    basedir = os.path.join(os.environ['decor'], subj,
                           '{}.{}.6mmblur.results'.format(subj, cond))
    infile = os.path.join(basedir,
                          'errts.{}.{}.6mmblur_REML+orig'.format(subj, cond))
    log.info('Do allineate %s %s', subj, cond)
    aff_sufx = 'sess2_6mmblur_meanepi_gm_mat.aff12.1D'
    cmdargs = split('3dAllineate -cubic -base {ss}_sess1_6mmblur_meanepi+orig \
                    -1Dmatrix_apply {ss}_{aff_sufx} \
                    -prefix errts.{ss}.{cc}.6mmblur_REML_gm \
                    -input {infile} -master SOURCE \
                    -weight_frac 1.0 -maxrot 6 -maxshf 10 -VERB \
                    -warp aff -source_automask+2 -twopass'.format(
                        ss=subj, aff_sufx=aff_sufx, cc=cond, infile=infile))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def copyn(log, subj, cond):
    """Copy errts into the dir and have contiguous naming convention."""
    log.info('Do copyn %s %s', subj, cond)
    basedir = os.path.join(os.environ['decor'], subj,
                           '{}.{}.6mmblur.results'.format(subj, cond))
    cmdargs = split('3dcopy {}/errts.{}.{}.6mmblur_REML+orig \
                    errts.{}.{}.6mmblur_REML_gm'.format(
                        basedir, subj, cond, subj, cond))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def build_subject_dict(subjectlist):
    """Build dictionary of subject and run orders."""
    orderfile = os.path.join(os.environ['decor'],
                             'SS_runs_presentation_orders_and_answers.csv')
    df = pd.read_csv(orderfile)
    stimdict = {}
    for subj in subjectlist:
        seriesorder = pd.Series(df.loc[df.SSname == subj, 'stim_name'])
        subjitem = {subj: {'sess1': list(seriesorder.iloc[:6]),
                    'sess2': list(seriesorder.iloc[6:])}}
        stimdict.update(subjitem)

    return stimdict


def do_avg_mean_epis(log, stimulus_dict, subj):
    """Average the epis and make mean."""
    for session in stimulus_dict[subj]:
        epilist = []
        for run in stimulus_dict[subj][session]:
            rundir = os.path.join(os.environ['decor'], subj,
                                  '{}.{}.6mmblur.results'.format(
                                      subj, run))
            fname = 'pb03.{}.{}.6mmblur.r01.volreg+orig'.format(
                subj, run)
            epilist.append(os.path.join(rundir, fname))

        epilist = ' '.join(epilist)
        avgepis(log, subj, session, epilist)
        mean_sess(log, subj, session)


def dir_check(directory):
    """Create the directory is not exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    """Wrap all the methods to execute."""
    subject_list = ['PMBI', 'LNDR', 'ANRC', 'DAHL']
    subjectstim_dict = build_subject_dict(subject_list)
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                        'align_epis'))
    logfile.info('started 5.align_epis.py')

    for subject in subject_list:
        resultsdir = os.path.join(os.environ['decor'], subject,
                                  '6mmblur_results')
        dir_check(resultsdir)
        os.chdir(resultsdir)
        print(os.getcwd())
        do_avg_mean_epis(logfile, subjectstim_dict, subject)
        align_epis(logfile, subject)
        for run in subjectstim_dict[subject]['sess2']:
            allineate(logfile, subject, run)

        for run in subjectstim_dict[subject]['sess1']:
            copyn(logfile, subject, run)


if __name__ == "__main__":
    main()
