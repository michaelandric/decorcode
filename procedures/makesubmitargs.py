#!/usr/bin/python

from optparse import OptionParser

class MakeArgs:

    def get_opts(self):
        desc = """Program for generating condor_submit arguments. Run this with 'exec_makesubmitargs.py' to iterate arguments."""
        self.usage = "usage: %prog [options]"
        self.parser = OptionParser(description=desc, version="%prog October.2012")
        self.parser.add_option("--subject", dest="subject",
                               help="specify the subject")
        self.parser.add_option("--arg1", dest="arg1",
                               help="first argument")
        self.parser.add_option("--arg2", dest="arg2",
                               help="second argument")
        self.parser.add_option("--arg3", dest="arg3",
                               help="third argument")
        self.parser.add_option("--arg4", dest="arg4",
                               help="fourth argument")

        (self.options, args) = self.parser.parse_args()



    def construct_to3d(self, subject):
        """
        """
        print "arguments    = --Subject "+subject+" --tlrc_brain "+subject+"tlrc+tlrc \nqueue \n"


makeargs = MakeArgs()
