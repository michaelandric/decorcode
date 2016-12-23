# -*- coding: utf-8 -*-
"""Created Dec 2016.

Implement basic 3dCalc commands.
@author: andric.
"""

import os
from shlex import split
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT
from setlog import setup_log


def conjunciton_overlap(log, afile, bfile, cfile, outname):
    """Overlap different functional images.

    expr arg is expression in 3dcalc
    e.g., step(a)+2*step(b)
    e.g., ispositive(a-b) + 2*ispositive(a-c)
    """
    log.info("Overlap func datasets.")
    log.info("Output: %s", outname)
    cmdargs = split("3dcalc -a %s -b %s -c %s \
                    -expr 'ispositive(a-b) + 2*ispositive(a-c)' -prefix %s" %
                    (afile, bfile, cfile, outname))
    proc = Popen(cmdargs, stdout=PIPE, stderr=STDOUT)
    log.info(proc.stdout.read())


def main():
    """Call methods for thresholding and clustering."""
    logfile = setup_log(os.path.join(os.environ['decor'], 'logs',
                                     'do_conj_mask'))
    logfile.info('Threshold and cluster.')
    os.chdir(os.path.join(os.environ['decor'], 'randomise_repmeas'))

    suff = 'corrp_tstat1_thr001fwe05'
    for ctype in ['clustere', 'clusterm', 'tfce']:
        conjunciton_overlap(logfile,
                            'AV_out_1tailp001_n5000_{}_{}.nii.gz'.format(ctype, suff),
                            'A_out_1tailp001_n5000_{}_{}.nii.gz'.format(ctype, suff),
                            'V_out_1tailp001_n5000_{}_{}.nii.gz'.format(ctype, suff),
                            'conj_3set_1tailp001_n5000_{}_{}'.format(ctype, suff))


if __name__ == '__main__':
    main()
