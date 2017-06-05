#!/usr/bin/env python2.7
"""
Run a regresion test on a sense amp array
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 09_sense_amp_test")


class sense_amp_test(unittest.TestCase):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))

        import sense_amp_array


        debug.info(2, "Testing sense_amp_array for word_size=4, words_per_row=2")
        OPTS.check_lvsdrc = False
        a = sense_amp_array.sense_amp_array(word_size=4, words_per_row=2)
        OPTS.check_lvsdrc = True
        self.local_check(a)

        globals.end_openram()
        
    def local_check(self, a):
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        self.assertFalse(calibre.run_drc(a.name, tempgds))
        self.assertFalse(calibre.run_lvs(a.name, tempgds, tempspice))

        os.remove(tempspice)
        os.remove(tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
