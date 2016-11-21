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
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'thresh_cluster_fsl'))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))

    pref = 'repmeas_randomise_out_n5000'
    for i in range(1, 5):
        fsl_maths(logfile,
                  '{}_clustere_corrp_tstat{}'.format(i, pref),
                  '{}_tstat{}.nii.gz'.format(i, pref),
                  '{}_clustere_corrp_tstat{}_thr'.format(i, pref))
        cluster(logfile,
                '{}_clustere_corrp_tstat{}_thr.nii.gz'.format(i, pref),
                '{}_clustere_corrp_tstat{}_thr_cluster_size'.format(i, pref),
                '{}_clustere_corrp_tstat{}_thr_lmax.txt'.format(i, pref),
                '{}_clustere_corrp_tstat{}_thr_cluster_size'.format(i, pref))

if __name__ == '__main__':
    main()
