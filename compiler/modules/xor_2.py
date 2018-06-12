import design
import debug
import utils
from tech import GDS,layer

class xor_2(design.design):

    pin_names = ["a", "b", "out", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("xor_2", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "xor_2", GDS["unit"], layer["boundary"])

    def __init__(self, name="xor_2"):
        design.design.__init__(self, name)
        debug.info(2, "Create 2 input xor gate")

        self.width = xor_2.width
        self.height = xor_2.height
        self.pin_map = xor_2.pin_map

    def analytical_delay(self, slew, load=0.0):
      #TODO
      debug.info(2, "xor2 analytical delay...")

    def analytical_power(self, proc, vdd, temp, load):
      #TODO
      debug.info(2, "xor2 analytical delay...")
