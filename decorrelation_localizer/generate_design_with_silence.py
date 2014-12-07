#!/usr/bin/python

"""Check the file paths.
This is set to run from PycharmProjects dir on local mac"""

import numpy as np
from shlex import split
from subprocess import call
from subprocess import STDOUT
from subprocess import Popen
from subprocess import PIPE


class GenDesign:

    def __init__(self, cond1starts, cond2starts, rnd_sent_durs, nrm_sent_durs):
        print 'Initializing'
        self.start_times_Rnd = np.array(np.loadtxt(cond1starts))   # these are in seconds
        self.start_times_Nrm = np.array(np.loadtxt(cond2starts))   # these are in seconds
        self.sentence_durations_Rnd = np.array(np.loadtxt(rnd_sent_durs))   # in seconds
        self.sentence_durations_Nrm = np.array(np.loadtxt(nrm_sent_durs))  # in seconds
        print 'Input files OK'
        self.numbers_rnd = np.random.choice(range(1, 25), size=12, replace=False)   # because 12 of each stim in run
        self.numbers_nrm = np.random.choice(self.numbers_rnd, size=12, replace=False)
        self.TR = 1.5   # seconds
        self.run_length = 324   # seconds

    def get_silent_gaps(self):
        """get the gaps in seconds between stimuli sentences"""
        end_times_rnd = []
        end_times_nrm = []
        for i in xrange(len(self.numbers_rnd)):
            end_times_rnd.append(self.start_times_Rnd[i] + self.sentence_durations_Rnd[self.numbers_rnd[i]-1][1])
            end_times_nrm.append(self.start_times_Nrm[i] + self.sentence_durations_Nrm[self.numbers_nrm[i]-1][1])

        starts = np.append(self.start_times_Nrm, self.start_times_Rnd)
        ends = np.append(end_times_nrm, end_times_rnd)
        timing_arr = np.append(starts, ends)
        timing_arr.sort()
        timing_arr = np.insert(timing_arr, 0, 0)   # put a 0 to mark first and set up gap difference measures
        timing_arr = np.append(timing_arr, self.run_length)   # put the end (in sec) to set up difference measures

        gaps = np.diff(timing_arr)
        gaps = gaps[range(0, len(gaps), 2)]
        return gaps

    def make_silent_wavs(self, gapdiffs, outdir):
        """Make silent segments between sentences"""
        durationlist = []
        for i, g in enumerate(gapdiffs):
            num = i+1
            gg = g-.01
            f = open('%sstdout_files/stdout_from_make_silent_wavs.txt' % outdir, 'w')
            cmdargs = split('ffmpeg -f lavfi -i aevalsrc=0:0:0:0:0:0::duration=%(gg)s -ac 1 -ab 705 %(outdir)ssilence%(num)s.wav' % locals())
            call(cmdargs, stdout=f, stderr=STDOUT)
            f.close()
            cmdargs = split('ffmpeg -i %(outdir)ssilence%(num)s.wav' % locals())
            aa = Popen(cmdargs, stderr=PIPE)
            aout = aa.stderr.read()
            for line in aout.split('\n'):
                if 'Duration' in line:
                    durationlist.append(line)

        durations = [float(ll.split()[1].split(',')[0].split(':')[2]) for ll in durationlist]
        outf = open('%sduration_silent_segments.txt' % outdir, 'w')
        durs = ""
        for d in enumerate(durations):
            differ = round(d[1] - gapdiffs[d[0]], 4)
            durs += `d[0]+1`+' '+`d[1]`+' '+`round(gapdiffs[d[0]], 4)`+' '+`differ`+'\n'

        outf.write(durs)
        outf.close()

    def make_file_list(self, outdir):
        """Compile file list that for 'concat' method in ffmpeg"""
        rnd_dict = dict(zip(self.start_times_Rnd, self.numbers_rnd))
        nrm_dict = dict(zip(self.start_times_Nrm, self.numbers_nrm))
        full_dict = dict(rnd_dict.items() + nrm_dict.items())
        sorted_starts = sorted(nrm_dict.keys() + rnd_dict.keys())
        stims = []
        stimsduration = []
        for i in sorted_starts:
            if i in rnd_dict.keys():
                stims.append("file 'Rndm_sentence_%s.wav'" % rnd_dict[i])
                stimsduration.append(rnd_dict[i])
            elif i in nrm_dict.keys():
                stims.append("file 'Nrml_sentence_%s.wav'" % nrm_dict[i])

        gaplist = []
        for i in xrange(1, 26):
            gaplist.append("file 'silence%s.wav'" % i)

        filelist = []
        for i, st in enumerate(stims):
            filelist.append(gaplist[i])
            filelist.append(stims[i])
        filelist.append(gaplist[len(gaplist)-1])   # this appends at end because there is one more silence than stim

        outfile = open('%(outdir)srun_stim_list.txt' % locals(), 'w')
        outfile.write('\n'.join(filelist))
        outfile.close()

    def make_file_list_for_sox(self, outdir):
        """Compile file list that for 'concat' method in ffmpeg"""
        rnd_dict = dict(zip(self.start_times_Rnd, self.numbers_rnd))
        nrm_dict = dict(zip(self.start_times_Nrm, self.numbers_nrm))
        full_dict = dict(rnd_dict.items() + nrm_dict.items())
        sorted_starts = sorted(nrm_dict.keys() + rnd_dict.keys())
        stims = []
        stimsduration = []
        for i in sorted_starts:
            if i in rnd_dict.keys():
                stims.append('Rndm_sentence_%s.wav' % rnd_dict[i])
                stimsduration.append(rnd_dict[i])
            elif i in nrm_dict.keys():
                stims.append('Nrml_sentence_%s.wav' % nrm_dict[i])

        gaplist = []
        for i in xrange(1, 26):
            gaplist.append('silence%s.wav' % i)

        filelist = []
        for i, st in enumerate(stims):
            filelist.append(gaplist[i])
            filelist.append(stims[i])
        filelist.append(gaplist[len(gaplist)-1])   # this appends at end because there is one more silence than stim

        outfile = open('%(outdir)srun_stim_list_for_sox.txt' % locals(), 'w')
        outfile.write(' '.join(filelist))
        outfile.close()
        return ' '.join(filelist)

    def make_experimental_run(self, outdir):
        """Combine individual silence and sentence files into run
        run this AFTER above functions, need 'run_stim_list.txt
        Below also shows alternate way to concat, using sox"""
        print 'Making the experimental run'
        f = open('%sstdout_files/stdout_from_make_experimental_run.txt' % outdir, 'w')
        cmdargs = split('ffmpeg -f concat -i %srun_stim_list.txt -c copy %ssentence_localizer_run1.wav' % (outdir, outdir))
        #cmdargs = split('sox --combine concatenate '+soxlist+' %ssentence_localizer_run1fromsox.wav' % outdir)
        call(cmdargs, stdout=f, stderr=STDOUT)
        f.close()
        print 'ALL GOOD'


if __name__ == "__main__":
    optim_timing_dir = '/Users/andric/Documents/workspace/decorrelation/localizers/optimize_timing/'
    sentencestims_dir = '/Users/andric/Documents/workspace/decorrelation/localizers/sentencestims/'
    cond1starts = optim_timing_dir+'condition_1_starts_i88.txt'
    cond2starts = optim_timing_dir+'condition_2_starts_i88.txt'
    rnd_sent_durs = sentencestims_dir+'duration_Rndm_sentences.txt'
    nrm_sent_durs = sentencestims_dir+'duration_Nrml_sentences.txt'
    gd = GenDesign(cond1starts, cond2starts, rnd_sent_durs, nrm_sent_durs)
    gaps = gd.get_silent_gaps()
    gd.make_silent_wavs(gaps, sentencestims_dir)
    gd.make_file_list(sentencestims_dir)
    gd.make_experimental_run(sentencestims_dir)

