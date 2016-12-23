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


def cluster(log, inputf, clustindx, lmax, omeanf, clustsize):
    """Cluster via FSL procedure."""
    log.info('Now doing cluster...')
    log.info('input file: ', inputf)
    log.info('clustindx: ', clustindx)
    cmdargs = split('cluster --in={} --thresh=0.001 --oindex={} \
                    --olmax={} --omean={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, omeanf, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster_addon_metric(log, inputf, clustindx, lmax, omeanf, clustsize):
    """Cluster via FSL procedure. Now also get mean for images."""
    log.info('Now doing cluster...')
    log.info('input file: %s', inputf)
    log.info('clustindx: %s', clustindx)
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
                    --olmax={} --omean={} --osize={} --mm'.format(
                        inputf, clustindx, lmax, omeanf, clustsize))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def cluster_omean(log, inputf, omeanf):
    """Cluster via FSL procedure. Get only mean for clusters."""
    log.info('Now doing cluster...')
    log.info('input file: %s', inputf)
    log.info('for omean: %s', omeanf)
    cmdargs = split('cluster --in={} --thresh=0.005 --omean={}'.format(
        inputf, omeanf))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    lname = 'thresh_cluster_fsl_thr001_fwe05'
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs', lname))
    logfile.info('Do threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))

    pref = 'out_1tailp001_n5000'
    conditions = ['AV', 'A', 'V', 'lowlev']
    for ctype in ['clustere', 'clusterm', 'tfce']:
        for cond in conditions:
            fsl_maths(logfile,
                      '{}_{}_{}_corrp_tstat1'.format(cond, pref, ctype),
                      '{}_{}_tstat1.nii.gz'.format(cond, pref),
                      '{}_{}_{}_corrp_tstat1_thr005fwe05'.format(cond, pref, ctype))
            cluster(logfile,
                    '{}_{}_{}_corrp_tstat1_thr001fwe05.nii.gz'.format(cond, pref, ctype),
                    '{}_{}_{}_corrp_tstat1_thr001fwe05_cluster_index'.format(cond, pref, ctype),
                    '{}_{}_{}_corrp_tstat1_thr001_fwe05lmax.txt'.format(cond, pref, ctype),
                    '{}_{}_{}_corrp_tstat1_thr001_fwe05omean'.format(cond, pref, ctype),
                    '{}_{}_{}_corrp_tstat1_thr001_fwe05cluster_size'.format(cond, pref, ctype))


if __name__ == '__main__':
    main()
