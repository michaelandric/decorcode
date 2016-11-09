# -*- coding: utf-8 -*-
"""
October 2016.

supplement to correct coding error made in 8.tcat_tcorrelate.py

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from setlog import setup_log
import tcat_tcorrelate as tc
import transform_corr as tr


def get_condition_mean(log, segments, subject, tcorrsffx):
    """Correlate segments into mean for condition."""
    episcond = []
    for m in ['AV', 'A', 'V', 'lowlev']:
        for seg in segments:
            episcond.append('{}_{}_{}_{}+orig'.format(
                seg, m, subject, tcorrsffx))
        epilist = ' '.join(episcond)
        pref = '{}_{}_{}_v2_mean'.format(m, subject, tcorrsffx)
        tc.mean_res(log, pref, epilist)


def main_wrap():
    """Wrap function call in main."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'tcat_tcorrelate'))
    logfile.info('Started 18.tcat_tcorrelate_z_transform.py')

    subj_list = ['VREA']

    __, clip, __ = tc.get_timings(logfile)
    segments = set(c.split('_')[0] for c in clip)

    for subject in subj_list:
        os.chdir(os.path.join(os.environ['decor'], subject, '6mmblur_results'))
        get_condition_mean(logfile, segments, subject,
                           '6mmblur_tcorr_out_spearman')
        for m in ['AV', 'A', 'V', 'lowlev']:
            tr.setnames_call_funcs(logfile, subject, m,
                                   '6mmblur_tcorr_out_spearman_v2')
        for funcseg in ['abouthalf', 'twothirds']:
            sub_segments = tc.subsettter(segments, funcseg)
            get_condition_mean(logfile, sub_segments, subject,
                               '6mmblur_tcorr_out_spearman_%s' % funcseg)
            for m in ['AV', 'A', 'V', 'lowlev']:
                tr.setnames_call_funcs(logfile, subject, m,
                                       '6mmblur_tcorr_out_v2_spearman_%s_v2' %
                                       funcseg)


if __name__ == '__main__':
    main_wrap()
