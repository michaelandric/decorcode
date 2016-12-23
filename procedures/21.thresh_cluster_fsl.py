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
    cmdargs = split('cluster --in={} --thresh=0.005 --oindex={} \
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
    lname = 'thresh_cluster_fsl_omean'
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs', lname))
    logfile.info('Already did threshold and cluster. Now just getting omean.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))

    pref = 'out_2tailp005_n5000'
    conditions = ['AV', 'A', 'V', 'lowlev']
    for ctype in ['clustere', 'clusterm', 'tfce']:
        for cond in conditions:
            cluster_omean(logfile,
                          '{}_{}_{}_corrp_tstat1_thr005fwe05.nii.gz'.format(cond, pref, ctype),
                          '{}_{}_{}_corrp_tstat1_thr005_fwe05omean'.format(cond, pref, ctype))


if __name__ == '__main__':
    main()
