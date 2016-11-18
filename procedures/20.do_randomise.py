# -*- coding: utf-8 -*-
"""
Created Nov 15 2016.

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
import numpy as np
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
    for subject in subj_list:
        for cond in conditions_list:
            filelist.append(os.path.join(
                os.environ['decor'], subject, '6mmblur_results',
                'highres_fnirted_MNI2mm_%s_%s_6mmblur_v2_Z.nii.gz'
                % (subject, cond)))

    return ' '.join(filelist)


def make_design_mat_reptmeas(subj_list, conditions_list):
    """Build design matrix for FSL process.

    Make what fsl docs call 'design.mat'
    """
    subjmat = np.zeros((len(conditions_list), len(conditions_list)))
    np.fill_diagonal(subjmat, 1)

    b = np.repeat(np.zeros(len(conditions_list)*len(subj_list)),
                  len(subj_list)).reshape(
                      len(conditions_list)*len(subj_list), len(subj_list))
    for i, _ in enumerate(subj_list):
        row_start = i*len(conditions_list)
        row_stop = i*len(conditions_list)+len(conditions_list)
        b[row_start:row_stop, i] = np.repeat(1, len(conditions_list))
    return np.column_stack((b, np.vstack([subjmat]*len(subj_list))))


def make_design_grp_repeatmeas(subj_list, conditions_list):
    """Build group design file for fsl.

    This makes what fsl docs call 'design.grp'
    """
    return np.array(range(1, len(subj_list)+1)).repeat(len(conditions_list))


def old_make_design_contr_repeatmeas(subj_list, conditions_list):
    """Get the contr vector.

    This makes what fsl docs call 'design.con'
    """
    subjmat = np.zeros((len(conditions_list), len(conditions_list)))
    np.fill_diagonal(subjmat, 1)

    subjarr = np.zeros((len(conditions_list)) * len(subj_list)).reshape(
        (len(conditions_list)), len(subj_list))
    return np.column_stack((subjarr, subjmat))


def make_design_contr_repeat_meas():
    """Build contrast matrix."""
    a = np.array((3, -1, -1, -1))
    return np.vstack((a, np.roll(a, 1), np.roll(a, 2), np.roll(a, 3)))


def make_design_f_contr(conditions_list):
    """Derive f contrast from conditions."""
    return np.repeat(1, len(conditions_list))


def fsl_randomise(log, inputf, outpref):
    """Randomise in fsl."""
    log.info('Starting fsl randomise...')
    try:
        cmdargs = split('randomise -i {} -o {} -d design.mat -t design.con \
                        -f design.fts -e design.grp -m mask -T'.format(
                            inputf, outpref))
        proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
        log.info(proc.stdout.read())
    except proc as err:
        print('SOMETHING BROKE ---------- randomise NOT WORKING: ', err.value)


def setup_randomise(log, workdir, subj_list, conditions_list):
    """Build 4D file. Create design files."""
    log.info('Started make and merge fsl 4D file...')
    four_d_file = 'repmeas_4Dfile'
    mergefsl(log, make_file_list(subj_list, conditions_list),
             os.path.join(workdir, four_d_file))

    log.info('Started making design files...')
    np.savetxt(os.path.join(workdir, 'design.con'),
               make_design_contr_repeat_meas(), fmt='%i')
    np.savetxt(os.path.join(workdir, 'design.grp'),
               make_design_grp_repeatmeas(subj_list, conditions_list),
               fmt='%i')
    np.savetxt(os.path.join(workdir, 'design.mat'),
               make_design_mat_reptmeas(subj_list, conditions_list), fmt='%i')
    np.savetxt(os.path.join(workdir, 'design.fts'),
               make_design_f_contr(conditions_list), fmt='%i')


def main():
    """Call methods to get randomise."""
    randomise_dir = os.path.join(os.environ['decor'], 'randomise_repmeas')
    conditions = ['AV', 'A', 'V', 'lowlev']
    subjects = ['NNPT', 'SSGO', 'LSRS', 'SEKI',
                'LNSE', 'JNWL', 'PMBI', 'LNDR',
                'GOPR', 'DAHL', 'RSDE', 'VREA']
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'do_randomise'))
    setup_randomise(logfile, randomise_dir, subjects, conditions)
#     os.chdir(randomise_dir)
#     logfile.info('Now in working directory: %s', os.getcwd())
#     fsl_randomise(logfile,
#                   os.path.join(workdir, 'repmeas_4Dfile'),
#                   os.path.join(workdir, 'repmeas_randomise_out'))
