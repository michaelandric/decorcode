# -*- coding: utf-8 -*-
"""
Code overhaul on June 10 2016.

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def afni_tcat(log, subj, pref, epi_list):
    """Concat the epi list."""
    log.info('Doing tcat %s, %s', subj, pref)
    cmdargs = split('3dTcat -prefix {} {}'.format(pref, epi_list))
    try:
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info('cmd: \n%s', cmdargs)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE----------TCAT NOT WORKING: ', err.value)


def afni_tcorr(log, pref, epi_cat1, epi_cat2):
    """Do 3dTcorrelate."""
    log.info('Doing tcorr %s', pref)
    cmdargs = split('3dTcorrelate -polort -1 -spearman \
                    -prefix {} {} {}'.format(pref, epi_cat1, epi_cat2))
    log.info('cmd: \n%s', cmdargs)
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def mean_res(log, pref, epis):
    """Average the list of epis.

    In this version, 'epis' is a list of epis
    """
    log.info('Doing mean_res')
    cmdargs = split('3dMean -prefix {} {}'.format(pref, epis))
    log.info('cmd: \n%s', cmdargs)
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
    return (run, clip, trs)


def subsettter(clipsegments, lengthtype):
    """Subset the amount of time segments used in the analyses.

    Args:
        clipsegments: a list of clip segments
        lengthtype: Either 'twothirds' to use 2/3 of the data
                    or
                    'abouthalf' to use about 1/2 of the data

    Playing with shortening the amount of data
    where "ttm" is a modified version of above "tt" list,
     in which each start and stop TR are strip(':')
    so each is a tuple.
    then quick glimpse to calculate TRs used...

    e.g., for "*twothirds" results
    >>> sum([i[1] - i[0] for ii, i  in enumerate(ttm) if
     clipseg[ii] != 'AF13' and clipseg[ii] != 'AR8'])/1959.
    >>> 0.63093415007656972
    >>>

    This is for "abouthalf" data
    >>> sum([i[1] - i[0] for ii, i  in enumerate(ttm) if
     clipseg[ii] != 'AF13' and clipseg[ii] != 'AR8' and
     clipseg[ii] != 'AF7'])/1959.
    >>> 0.52220520673813176
    """
    if lengthtype == 'twothirds':
        clipsegments.remove('AR8')
        clipsegments.remove('AF13')
    elif lengthtype == 'abouthalf':
        clipsegments.remove('AR8')
        clipsegments.remove('AF13')
        clipsegments.remove('AF7')
    return clipsegments


def tcorr_main(log, subject, segments, tcorrsffx):
    """Correlate different segments and conditions."""
    os.chdir(os.path.join(os.environ['decor'], subject, '6mmblur_results'))
    for seg in segments:
        # This is for the AV correlations
        epi1 = '{}_AV.1_{}_splicy+orig'.format(seg, subject)
        epi2 = '{}_AV.2_{}_splicy+orig'.format(seg, subject)
        pref = '{}_AV_{}_{}'.format(seg, subject, tcorrsffx)
        afni_tcorr(log, pref, epi1, epi2)

        # This is to get low level visual and auditory correlations
        epi1 = '{}_V_{}_splicy+orig'.format(seg, subject)
        epi2 = '{}_A_{}_splicy+orig'.format(seg, subject)
        pref = '{}_lowlev_{}_{}'.format(seg, subject, tcorrsffx)
        afni_tcorr(log, pref, epi1, epi2)

        for m in ('V', 'A'):
            # These are for the V vs AV, A vs AV correlations
            for i in range(1, 3):
                epi1 = '{}_{}_{}_splicy+orig'.format(seg, m, subject)
                epi2 = '{}_AV.{}_{}_splicy+orig.'.format(seg, i, subject)
                pref = '{}_{}.{}_{}_{}'.format(seg, m, i, subject, tcorrsffx)
                afni_tcorr(log, pref, epi1, epi2)

            epis = []
            for i in range(1, 3):
                epis.append('{}_{}.{}_{}_{}+orig'.format(
                    seg, m, i, subject, tcorrsffx))
            epi_list = ' '.join(epis)
            pref = '{}_{}_{}_{}+orig'.format(seg, m, subject, tcorrsffx)
            mean_res(log, pref, epi_list)

    """Below revises prior flawed version.
    Had used same epis list as prior call, so
    was including erroneous segments together.
    """
    episcond = []
    for m in ['AV', 'A', 'V', 'lowlev']:
        for seg in segments:
            episcond.append('{}_{}_{}_{}+orig'.format(
                seg, m, subject, tcorrsffx))
        epilist = ' '.join(episcond)
        pref = '{}_{}_{}_mean'.format(m, subject, tcorrsffx)
        mean_res(log, pref, epilist)


def main():
    """Do methods above via this wrapper."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'tcat_tcorrelate'))
    logfile.info('Started 8.tcat_tcorrelate.py')

    subj_list = ['RSDE', 'VREA']

    # Below is for full time series.
    __, clip, __ = get_timings(logfile)
    segments = set(c.split('_')[0] for c in clip)
    tcorr_suf = '6mmblur_tcorr_out_spearman'
    for subject in subj_list:
        tcorr_main(logfile, subject, segments, tcorr_suf)

    # Below is for subset of time series.
    # When run either 'twothirds' or 'abouthalf'.
    """
    run, clip, trs = get_timings(logfile)
    for funcseg in ['abouthalf', 'twothirds']:
        segments = set(c.split('_')[0] for c in clip)
        segments = subsettter(segments, funcseg)
        tcorr_suf = '6mmblur_tcorr_out_spearman_{}'.format(funcseg)
        for subject in subj_list:
            tcorr_main(logfile, subject, segments, tcorr_suf)
    """

if __name__ == '__main__':
    main()
