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


def get_condition_mean(log, segments, cond, subject, tcorrsffx):
    """Correlate segments into mean for condition."""
    episcond = []
    for seg in segments:
        episcond.append('{}_{}_{}_{}+orig'.format(
            seg, cond, subject, tcorrsffx))
    epilist = ' '.join(episcond)
    pref = '{}_{}_{}_v2_mean'.format(cond, subject, tcorrsffx)
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
        for m in ['AV', 'A', 'V', 'lowlev']:
            get_condition_mean(logfile, segments, m, subject,
                               '6mmblur_tcorr_out_spearman')
            tr.setnames_call_funcs(logfile, subject, m,
                                   '6mmblur_tcorr_out_spearman_v2')
        for funcseg in ['abouthalf', 'twothirds']:
            segments = set(c.split('_')[0] for c in clip)
            sub_segments = tc.subsettter(segments, funcseg)
            for m in ['AV', 'A', 'V', 'lowlev']:
                get_condition_mean(logfile, sub_segments, m, subject,
                                   '6mmblur_tcorr_out_spearman_%s' % funcseg)
                tr.setnames_call_funcs(logfile, subject, m,
                                       '6mmblur_tcorr_out_spearman_%s_v2' %
                                       funcseg)


if __name__ == '__main__':
    main_wrap()
