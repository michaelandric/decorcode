# -*- coding: utf-8 -*-
"""
Created November 2016.

(AFNI doesn't work in 3+)

@author: andric
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def fsl_maths(log, corrp, statimg, outname):
    """Threshold via FSL procedure."""
    log.info('Doing fsl_maths to threshold the image...')
    cmdargs = split('fslmaths {} -thr 0.95 -bin -mul {} {}'.format(
        corrp, statimg, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster(log, inputf, clustindx, lmax, clustsize):
    """Cluster via FSL procedure."""
    log.info('Now doing cluster...')
    log.info('input file: ', inputf)
    log.info('clustindx: ', clustindx)
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'thresh_cluster_fsl_randomise_3set'))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_3set'))

    pref = 'repmeas_randomise3set_p005_n5000'
    for ctype in ['clustere', 'clusterm', 'tfce']:
        for i in range(1, 4):
            fsl_maths(logfile,
                      '{}_{}_corrp_tstat{}'.format(pref, ctype, i),
                      '{}_tstat{}.nii.gz'.format(pref, i),
                      '{}_{}_corrp_tstat{}_fwe05'.format(pref, ctype, i))
            cluster(logfile,
                    '{}_{}_corrp_tstat{}_fwe05.nii.gz'.format(pref, ctype, i),
                    '{}_{}_corrp_tstat{}_fwe05_cluster_index'.format(pref, ctype, i),
                    '{}_{}_corrp_tstat{}_fwe05lmax.txt'.format(pref, ctype, i),
                    '{}_{}_corrp_tstat{}_fwe05cluster_size'.format(pref, ctype, i))

if __name__ == '__main__':
    main()
