#!/usr/bin/python

"""Check the file paths.
This is set to run from PycharmProjects dir on local mac"""

import numpy as np
import pandas as pd

class LOGPARSE:

    def __init__(self, logf, outd, subjid):
        print 'Initializing'
        self.ss = subjid
        self.logfile = logf
        self.outdir = outd

    def parse_file(self):
        print 'READING LOGFILE'
        """ALTERNATE WAY:
        with open(item) as f:
            reader = csv.reader(f, delimiter = '\t')
            d = list(reader)
        """
        ff = pd.read_csv(self.logfile, sep = '\t')
        print 'DONE READING LOGFILE... \nNOW PARSING EVENTS AND TIMES...'
        codes = ff.loc[:,'Code']   # can also do 'codes = ff.iloc[:,3]'
        times = ff.loc[:,'Time']
        Etype = ff.loc[:,'Event Type']
        """Below gets where there was a pulse. Should be 406 of these. There are 14 pulses in a block,
        i.e., 14 * 1.5 s (the TR) = 21 s. Divide 406/14 = 29. There were 29 blocks total in the run."""
        tt = np.where(Etype.str.contains(r'Pulse'))[0]
        starts = np.array(times)[tt[range(0, len(tt), 14)]]
        end_conds = np.where(codes.str.contains(r'end_cond'))[0]

        print 'NOW FINDING CODES FROM BLOCKS...'
        blocks = []
        '''put in try and execpt for case where pulse hits too close together'''
        for e in end_conds:
            if np.array(codes)[e-1].split()[0] == '4':
                try:
                    blocks.append([np.array(codes)[e-3].split()[i] for i in [4, 8]])
                except:
                    blocks.append([np.array(codes)[e-5].split()[i] for i in [4, 8]])
            else:
                blocks.append([np.array(codes)[e-1].split()[i] for i in [4, 5]])

        """This finds the solo A or V blocks"""
        #solos = [b[0] for b in blocks if b[1].split('_')[0] == 'NO']
        solos_ind = [b for b in range(len(blocks)) if blocks[b][1].split('_')[0] == 'NO']
        """
        length_onlyAorV = len(solos)
        length_onlyA = len([s.split('_')[0] for s in solos if s.split('_')[0] == 'A'])
        length_onlyV = len([s.split('_')[0] for s in solos if s.split('_')[0] == 'V'])
        """

        vattn = []
        aattn = []
        print 'PARSING CONDITIONS...'
        for b in range(1, len(blocks)):
            if blocks[b][0] == 'V_ATTN':
                vattn.append(b)
            elif blocks[b][0] == 'A_ATTN':
                aattn.append(b)
        onlyA = [s for s in solos_ind if s in aattn]
        onlyV = [s for s in solos_ind if s in vattn]
        VATTN = [v for v in vattn if v not in onlyV]
        AATTN = [a for a in aattn if a not in onlyA]

        print 'WRITING OUTFILES...'
        '''They are written out in seconds (good for AFNI use)'''
        out_onlyA = open('%sonlyA.%s.txt' % (self.outdir, self.ss), 'w')
        out_onlyA.write(' '.join(map(str, starts[onlyA] / 10000.))+'\n')
        out_onlyA.close()

        out_onlyV = open('%sonlyV.%s.txt' % (self.outdir, self.ss), 'w')
        out_onlyV.write(' '.join(map(str, starts[onlyV] / 10000.))+'\n')
        out_onlyV.close()

        out_VATTN = open('%sVATTN.%s.txt' % (self.outdir, self.ss), 'w')
        out_VATTN.write(' '.join(map(str, starts[VATTN] / 10000.))+'\n')
        out_VATTN.close()

        out_AATTN = open('%sAATTN.%s.txt' % (self.outdir, self.ss), 'w')
        out_AATTN.write(' '.join(map(str, starts[AATTN] / 10000.))+'\n')
        out_AATTN.close()

        print 'DONE!'


if __name__ == "__main__":
    logdir = '/Users/andric/Documents/workspace/decorrelation/localizers/MJAcipetkov_TononoiseExpt/logfiles/'
    logfile = logdir+'001-tononoiseshrt99_EDIT.log'   # edit log file name
    subjid = 'IAGO'   # edit subject identifier
    lp = LOGPARSE(logfile, logdir, subjid)
    lp.parse_file()



