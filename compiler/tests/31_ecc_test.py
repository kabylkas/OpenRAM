#!/usr/bin/env python2.7
"""
Run a regresion test on ECC
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class ecc_test(openram_test):
    
    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = True
      
        import ecc
        debug.info(2, "Testing ECC for word_size=8")
        
        dut = ecc.ecc(word_size=4)
        self.local_check(dut)

        globals.end_openram()

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
