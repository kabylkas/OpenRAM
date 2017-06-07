import design
import debug
import utils
from tech import GDS,layer

class xor_2(design.design):

    pins = ["a", "b", "out", "vdd", "gnd"]
    chars = utils.auto_measure_libcell(pins, "xor_2", GDS["unit"], layer["boundary"])

    def __init__(self, name="xor_2"):
        design.design.__init__(self, name)
        debug.info(2, "Create 2 input xor gate")

        self.width = xor_2.chars["width"]
        self.height = xor_2.chars["height"]
