# -*- coding: utf-8 -*-
"""
Code overhaul on June 9 2016.

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def afni_splice(log, subj, pref, epi):
    """Splice the time series into conditions."""
    log.info('Doing splice %s, %s.', subj, pref)
    cmdargs = split('3dTcat -prefix {} {}'.format(pref, epi))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def tcat(log, subj, pref, epi_list):
    """Concat the epi list."""
    log.info('Doing tcat %s, %s', subj, pref)
    cmdargs = split('3dTcat -prefix {} {}'.format(pref, epi_list))
    try:
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE----------TCAT NOT WORKING: ', err.value)


def tcorr(log, subj, epi_cat1, epi_cat2):
    """Do 3dTcorrelate."""
    log.info('Doing tcorr %s', subj)
    cmdargs = split('3dTcorrelate -prefix corr_out_AV_{} {} {}'.format(
                    subj, epi_cat1, epi_cat2))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def get_timings(log):
    """Parse the timing file."""
    log.info('Doing get_timings')
    timingfile = os.path.join(os.environ['decor'], 'decorcode',
                              'stim_timing_info', 'Timing_layout.txt')
    timingf = open(timingfile, 'r')
    run = []
    clip = []
    trs = []
    for line in timingf:
        i, j, k = line.split()
        run.append(i)
        clip.append(j)
        trs.append(k)

    AV = [c for c in clip if c.split('_')[1] == 'AV']
    V = [c for c in clip if c.split('_')[1] == 'V']
    A = [c for c in clip if c.split('_')[1] == 'A']
    AV.sort()
    V.sort()
    A.sort()
    return (run, clip, trs)


def splice_conds(log, subj, runnum, movieclip, tmng):
    """Splice into conditions from the epi runs."""
    log.info('Doing splice_conds %s, %s, %s ', subj, movieclip, runnum)
    os.chdir(os.path.join(os.environ['decor'], subj, '6mmblur_results'))
    for i, cond in enumerate(movieclip):
        if 'AV' in runnum[i]:
            for j in range(1, 3):
                pref = '{}.{}_{}_splicy'.format(cond, j, subj)
                # Adding 7 and 3 TRs (10.5 and 4.5 s) to beginning and end
                a, b = map(int, tmng[i].split(":"))
                a = a + 7
                b = b + 3
                startstop = '{}..{}'.format(a, b)
                epidat = 'errts.{}.{}.{}.6mmblur_REML_gm+orig[{}]'.format(
                    subj, runnum[i], j, startstop)
                afni_splice(log, subj, pref, epidat)
        else:
            pref = '{}_{}_splicy'.format(cond, subj)
            a, b = map(int, tmng[i].split(":"))
            a = a + 7
            b = b + 3
            startstop = '{}..{}'.format(a, b)
            epidat = 'errts.{}.{}.6mmblur_REML_gm+orig[{}]'.format(
                subj, runnum[i], startstop)
            afni_splice(log, subj, pref, epidat)


def main():
    """Splice the time series and build condition sets."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'splice_tcat2'))
    logfile.info('Started 7.splice_tcat2.py')

    run, clip, tt = get_timings(logfile)

    subj_list = ['RSDE', 'VREA']
    for subject in subj_list:
        splice_conds(logfile, subject, run, clip, tt)

if __name__ == "__main__":
    main()
