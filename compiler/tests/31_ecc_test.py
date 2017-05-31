#!/usr/bin/env python2.7
"""
Run a regresion test on ECC
"""

import unittest
from testutils import header
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
import debug
import calibre

OPTS = globals.get_opts()

#@unittest.skip("SKIPPING 10_write_driver_test")


class ecc_test(unittest.TestCase):
    
    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        # we will manually run lvs/drc
        OPTS.check_lvsdrc = False
      
        import ecc
        debug.info(2, "Testing ECC for word_size=8")
        
        dut = ecc.ecc(word_size=8)
        self.local_check(dut)
        globals.end_openram()

  
    def local_check(self, dut):
        ecc_tempspice = OPTS.openram_temp + "ecc_temp.sp"
        ecc_tempgds = OPTS.openram_temp + "ecc_temp.gds"

        dut.sp_write(ecc_tempspice)
        dut.gds_write(ecc_tempgds)

        self.assertFalse(calibre.run_drc(dut.name, ecc_tempgds))
        #self.assertFalse(calibre.run_lvs(dut.name, ecc_tempgds, ecc_tempspice))

        os.remove(ecc_tempspice)
        os.remove(ecc_tempgds)

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
