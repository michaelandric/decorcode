# -*- coding: utf-8 -*-
"""
October 2016.

This has to run in Python 2.7 (AFNI doesn't work in 3+)
@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def dset_name(subject, condition, version=None):
    """Append the dataset names."""
    if version is None:
        return os.path.join(os.environ['decor'], subject, '6mmblur_results',
                            'highres_fnirted_MNI2mm_%s_%s_6mmblur_Z.nii.gz'
                            % subject, condition)
    else:
        return os.path.join(os.environ['decor'], subject, '6mmblur_results',
                            'highres_fnirted_MNI2mm_%s_%s_%s_6mmblur_Z.nii.gz'
                            % subject, condition, version)


def set_fnames(log, condition_list, subject_list):
    """Construct filenames for AFNI ANOVA."""
    log.info('Set names for dsets.')
    dsts = []
    amns = []
    for i, cond in enumerate(condition_list):
        amns.append("-amean %d %s_mean" % (i+1, cond))
        for j, subj in enumerate(subject_list):
            dsts.append("-dset %d %d '%s'" %
                        i+1, j+1, dset_name(subj, cond))

    return (amns, dsts)


def set_fnames_version(log, condition_list, subject_list, version):
    """Construct filenames for AFNI ANOVA."""
    log.info('Set names for dsets.')
    dsts = []
    amns = []
    for i, cond in enumerate(condition_list):
        amns.append("-amean %d %s_mean" % (i+1, cond))
        for j, subj in enumerate(subject_list):
            dsts.append("-dset %d %d '%s'" %
                        i+1, j+1, dset_name(subj, cond, version))

    return (amns, dsts)


def anova_afni(log, subjects, conditions, version=None):
    """Do AFNI 3dANOVA2."""
    log.info('Doing 3dANOVA2... ')
    if version is not None:
        a_means, d_sets = set_fnames_version(log, conditions,
                                             subjects, version)
        outname = os.path.join(os.environ['decor'], 'groupstuff',
                               'anova_out_6mmblur_%s' % version)
    else:
        a_means, d_sets = set_fnames(log, conditions, subjects)
        outname = os.path.join(os.environ['decor'], 'groupstuff',
                               'anova_out_6mmblur')
    cmdargs = split('3dANOVA2 -type 3 -alevels 4 -blevels %d %s \
                    -fa all_fstat %s -fab intxn_fstat -mask %s \
                    -acontr 3 -1 -1 -1 AV_contrast \
                    -acontr -1 3 -1 -1 A_constrast \
                    -acontr -1 -1 3 -1 V_contrast \
                    -acontr -1 -1 -1 3 lowlev_contr \
                    -bucket %s' %
                    (len(subjects),
                     ' '.join(d_sets),
                     ' '.join(a_means),
                     os.path.join(os.environ['fsl'], 'data/standard',
                                  'MNI152lin_T1_2mm_brain_mask.nii.gz'),
                     outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Wrap funciton calls to main."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'anova'))
    logfile.info('Started 17.anova.py')

    conditions_list = ['AV', 'A', 'V', 'lowlev']
    subjects_list = ['NNPT', 'SSGO', 'LSRS', 'SEKI',
                     'LNSE', 'JNWL', 'PMBI', 'LNDR',
                     'GOPR', 'DAHL', 'RSDE', 'VREA']

    anova_afni(logfile, subjects_list, conditions_list)
    for seg in ['twothirds', 'abouthalf']:
        anova_afni(logfile, subjects_list, conditions_list, seg)

if __name__ == '__main__':
    main()
