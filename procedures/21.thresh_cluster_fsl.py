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
                                     'thresh_cluster_fsl'))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))

    pref = 'out_2tailp005_n5000'
    conditions = ['AV', 'A', 'V', 'lowlev']
    for cond in conditions:
        fsl_maths(logfile,
                  '{}_{}_clustere_corrp_tstat1'.format(cond, pref),
                  '{}_{}_tstat1.nii.gz'.format(cond, pref),
                  '{}_{}_clustere_corrp_tstat1_thr005fwe05'.format(cond, pref))
        cluster(logfile,
                '{}_{}_clustere_corrp_tstat1_thr005fwe05.nii.gz'.format(cond, pref),
                '{}_{}_clustere_corrp_tstat1_thr005fwe05_cluster_index'.format(cond, pref),
                '{}_{}_clustere_corrp_tstat1_thr005_fwe05lmax.txt'.format(cond, pref),
                '{}_{}_clustere_corrp_tstat1_thr005_fwe05cluster_size'.format(cond, pref))

if __name__ == '__main__':
    main()
