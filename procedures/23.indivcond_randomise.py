# -*- coding: utf-8 -*-
"""
Created Nov 25 2016.

Build individual condition 4D files.
Then will do t-tests.

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log
import do_randomise as dr


def indvcond_make_file_list(subj_list, condition):
    """Make list of files.

    File names are hard coded in here. Change here if adjusting
    the file origins.
    """
    filelist = []
    for subject in subj_list:
        filelist.append(os.path.join(
            os.environ['decor'], subject, '6mmblur_results',
            'highres_fnirted_MNI2mm_%s_%s_6mmblur_v2_Z.nii.gz'
            % (subject, condition)))

    return ' '.join(filelist)


def make_condition_file(log, rnd_dir, conditions, subjects):
    """Make individual condition files."""
    for cond in conditions:
        four_d_file = '%s_4Dfile' % cond
        log.info('Make file %s', four_d_file)
        dr.mergefsl(log, indvcond_make_file_list(subjects, cond),
                    os.path.join(rnd_dir, four_d_file))


def indiv_t_randomise(log, n_reps, inputf, outpref):
    """Randomise in fsl."""
    log.info('Starting fsl randomise...')
    try:
        cmdargs = split('randomise -i %s -o %s -1 -v 5 \
                        -C 3.497 -c 3.497 -T -n %d' %
                        (inputf, outpref,
                         os.path.join(os.environ['FSLDIR'], 'data/standard',
                                      'MNI152lin_T1_2mm_brain_mask.nii.gz'),
                         n_reps))
        print('Command: \n')
        print('%s\n' % cmdargs)
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE ---------- randomise NOT WORKING: ', err.value)


def main():
    """Wrap funciton call."""
    randomise_dir = os.path.join(os.environ['decor'], 'randomise_repmeas')
    conditions = ['AV', 'A', 'V', 'lowlev']
    subjects = ['NNPT', 'SSGO', 'LSRS', 'SEKI',
                'LNSE', 'JNWL', 'PMBI', 'LNDR',
                'GOPR', 'DAHL', 'RSDE', 'VREA']
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'indivcond_randomise'))
    nreps = 10
    os.chdir(randomise_dir)
    logfile.info('Now in working directory: %s', os.getcwd())
    make_condition_file(logfile, randomise_dir, conditions, subjects)
    for cond in conditions:
        indiv_t_randomise(logfile, nreps,
                          os.path.join(randomise_dir, '%s_4Dfile' % cond),
                          os.path.join(randomise_dir,
                                       '%s_out_2tailp005_n%d' % (cond, nreps)))


if __name__ == '__main__':
    main()
