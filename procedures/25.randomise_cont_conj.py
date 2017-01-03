# -*- coding: utf-8 -*-
"""
Created Dec 2016.

(AFNI doesn't work in 3+)
Includes a setup_randomise function.
setup_randomise builds and writes the 4D file and the design files.
Both are murky fsl necessities.
IMPORTANT: Will have to go back and add header info to design files.
I do them by hand until wholly clear about their formatting.

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def mergefsl(log, file_list, outname):
    """Merge files with fslmerge."""
    log.info('Started merge fsl 4D file...')
    cmdargs = split('fslmerge -t {} {}'.format(outname, file_list))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def make_file_list(subj_list, conditions_list):
    """Make list of files.

    File names are hard coded in here. Change here if adjusting
    the file origins.
    """
    filelist = []
    for cond in conditions_list:
        for subject in subj_list:
            filelist.append(os.path.join(
                os.environ['decor'], subject, '6mmblur_results',
                'highres_fnirted_MNI2mm_%s_%s_6mmblur_v2_Z.nii.gz'
                % (subject, cond)))

    return ' '.join(filelist)


def fsl_randomise(log, n_reps, inputf, outpref):
    """Randomise in fsl."""
    log.info('Starting fsl randomise...')
    try:
        cmdargs = split('randomise -i %s -o %s -d design.mat -t design.con \
                        -f design.fts -e design.grp -m %s \
                        -C 3.106 -c 3.106 -T -n %d' %
                        (inputf, outpref,
                         os.path.join(os.environ['FSLDIR'], 'data/standard',
                                      'MNI152lin_T1_2mm_brain_mask.nii.gz'),
                         n_reps))
        print 'Command: \n'
        print '%s\n' % cmdargs
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE ---------- randomise NOT WORKING: ', err.value)


def main():
    """Call methods to get randomise."""
    randomise_dir = os.path.join(os.environ['decor'],
                                 'randomise_twocond_contr_conj')
    subjects = ['NNPT', 'SSGO', 'LSRS', 'SEKI',
                'LNSE', 'JNWL', 'PMBI', 'LNDR',
                'GOPR', 'DAHL', 'RSDE', 'VREA']
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'do_randomise_twocond_contr_conj'))
    os.chdir(randomise_dir)
    nreps = 5000

    mergefsl(logfile, make_file_list(subjects, ['AV', 'A']), 'AVvA_4Dfile')
    fsl_randomise(logfile, nreps,
                  os.path.join(randomise_dir, 'AVvA_4Dfile'),
                  os.path.join(randomise_dir,
                               'AVvA_randomise_out_n%d_p005' % nreps))

    mergefsl(logfile, make_file_list(subjects, ['AV', 'V']), 'AVvV_4Dfile')
    fsl_randomise(logfile, nreps,
                  os.path.join(randomise_dir, 'AVvV_4Dfile'),
                  os.path.join(randomise_dir,
                               'AVvV_randomise_out_n%d_p005' % nreps))


if __name__ == '__main__':
    main()
