import design
from tech import drc
from vector import vector
import debug
from globals import OPTS
import math
import sys, os
sys.path.append(os.path.join(sys.path[0],"router"))
import router
from nand_2 import nand_2
from nand_3 import nand_3
from pinv import pinv
class ecc(design.design):
    """
    Error correction code Write module. Generates parity bits based on Hamming Code
    Single Error Correction Double Error Detection algorithm. Dynamically creates
    parity bit generation logic with 2 input XOR gate.
    """

    def __init__(self, word_size):
        design.design.__init__(self, "ecc")
        debug.info(1, "Creating {0}".format(self.name))

        c = reload(__import__(OPTS.config.xor_2))
        self.mod_xor_2 = getattr(c, OPTS.config.xor_2)
        self.xor_2_chars = self.mod_xor_2.chars

        self.word_size = word_size
        self.parity_num = int(math.floor(math.log(word_size,2)))+1;

        self.add_pins()
        self.create_layout()
        #self.DRC_LVS()

    def add_pins(self):
        #add input pins
        """
        for i in range(self.word_size):
            self.add_pin("ecc_data_in[{0}]".format(i))

        #add output pins (generated parity bits)
        for i in range(self.parity_num):
            self.add_pin("ecc_parity_out[{0}]".format(i))
        """
        #vdd and gnd
        self.add_pin("vdd")
        self.add_pin("gnd")

    def create_layout(self):
        self.create_xor_2()
        self.setup_layout_constants()
        self.add_parity_generator()
        self.route_parity_generator()
        #self.add_syndrome_generator()
        #self.route_syndrom_generator()
        #self.create_nand_2()
        #self.create_nand_3()
        #self.create_pinv()
        #self.add_decoder()

    def create_xor_2(self):
        self.xor_2 = self.mod_xor_2("xor_2")
        self.add_mod(self.xor_2)

    def create_nand_2(self):
        self.nand_2 = nand_2(name="pnand2",
                             nmos_width=4,
                             height=self.xor_2.height)
        self.add_mod(self.nand_2)

    def create_nand_3(self):
        self.nand_3 = nand_3(name="pnand3",
                             nmos_width=4,
                             height=self.xor_2.height)
        self.add_mod(self.nand_2)

    def create_pinv(self):
        self.inv = pinv(name="pinv",
                    nmos_width=4,
                    height=self.xor_2.height)
        self.add_mod(self.nand_2)

    def setup_layout_constants(self):
        self.vdd_positions = []
        self.gnd_positions = []
        self.a_positions = []
        self.b_positions = []
        self.out_positions = []
        self.xor_2_positions = []
        self.xor_2_connections = []

    def add_parity_generator(self):
        print "laying out xor2 gates..."
        #calculate total number of bits
        total_bit_num = self.word_size+self.parity_num

        #generate xor2 gate set for each parity bit
        for parity_i in range(self.parity_num):
            #calculate number of inputs for the current parity
            two_to_parity_i = int(math.pow(2, parity_i))
            check = True
            input_num = 0
            count = 0
            for bit in range(two_to_parity_i, total_bit_num):
                count = count + 1
                if check:
                    input_num = input_num + 1
                if count == two_to_parity_i:
                    count = 0
                    check = not check

            #subtract 1 from the calculated input number
            input_num = input_num - 1

            #xor2 gate number is equal two input number - 1
            gate_num = input_num-1
            gate_num_half = int(math.floor(gate_num/2))
            for i in range(gate_num):
                name = "ecc_xor2_{0}_{1}".format(parity_i, i)
                if i<gate_num_half:
                    direction = "R0"
                    xoffset = i
                    yoffset = 2*parity_i*(self.xor_2.height)
                else:
                    direction = "MX"
                    xoffset = i-int(math.floor(gate_num/2))
                    yoffset = (2*parity_i+2)*(self.xor_2.height)

                a_flip_offset = vector(0,0)
                b_flip_offset = vector(0,0)
                out_flip_offset = vector(0,0)
                if direction == "MX":
                    xor_2_h = self.xor_2.height
                    ab_y_distance = self.xor_2_chars["a"][1]-self.xor_2_chars["b"][1]
                    #a
                    a_y = xor_2_h+ab_y_distance
                    a_flip_offset = vector(0,a_y)
                    #b
                    b_y = xor_2_h-ab_y_distance
                    b_flip_offset = vector(0, b_y)
                    #out
                    out_y = xor_2_h-(xor_2_h-2*self.xor_2_chars["out"][1])
                    out_flip_offset = vector(0, out_y)

                xor_2_position = vector(self.xor_2.width * xoffset, yoffset)
                a_offset = xor_2_position+\
                           vector(self.xor_2_chars["a"][0], self.xor_2_chars["a"][1])-\
                           a_flip_offset
                b_offset = xor_2_position+\
                           vector(self.xor_2_chars["b"][0], self.xor_2_chars["b"][1])-\
                           b_flip_offset
                out_offset = xor_2_position+\
                             vector(self.xor_2_chars["out"][0], self.xor_2_chars["out"][1])-\
                             out_flip_offset

                #add current xor2 to the design
                self.add_inst(name = name, 
                              mod = self.xor_2,
                              offset = xor_2_position,
                              mirror = direction)

                self.xor_2_positions.append(xor_2_position)

                #add labels
                self.add_label(text = "a_{0}_{1}".format(parity_i, i),
                               layer = "metal2",
                               offset = a_offset)
                self.add_label(text = "b_{0}_{1}".format(parity_i, i),
                               layer = "metal2",
                               offset = b_offset)
                self.add_label(text = "out_{0}_{1}".format(parity_i, i),
                               layer = "metal2",
                               offset = out_offset)

                self.add_pin("a_{0}_{1}".format(parity_i, i))
                self.add_pin("b_{0}_{1}".format(parity_i, i))
                self.add_pin("out_{0}_{1}".format(parity_i, i))
                #connect
                self.connect_inst(["a_{0}_{1}".format(parity_i, i),
                                   "b_{0}_{1}".format(parity_i, i),
                                   "out_{0}_{1}".format(parity_i, i),
                                   "vdd",
                                   "gnd"])

            #add vdd and gnd labels
            for i in range(2*self.parity_num+1):
                pin_name = "gnd"
                if i%2:
                    pin_name = "vdd"
                
                label_offset = vector(0, i*(self.xor_2.height-self.xor_2.rails_height)+self.xor_2.rails_height/2)
                self.add_label(text = pin_name,
                               layer = "metal1",
                               offset = label_offset)
  

            self.gds_write(OPTS.openram_temp+"xor2s.gds")

            #generate connections between xor gates in the upper row 
            dst = 0
            src = gate_num_half
            while dst<gate_num_half:
                xor_2_connection = ("out_{0}_{1}".format(parity_i, src), "a_{0}_{1}".format(parity_i, dst))
                self.xor_2_connections.append(xor_2_connection)
                if src+1<gate_num:
                    xor_2_connection = ("out_{0}_{1}".format(parity_i, src+1), "b_{0}_{1}".format(parity_i, dst))
                    self.xor_2_connections.append(xor_2_connection)
                dst=dst+2
                src=src+2

            #generate connections between xor gates in the bottom row
            inc = 1
            done = False
            while not done:
                offset = inc
                first_iteration = True
                while offset<=gate_num_half:
                    first = offset
                    second = offset + inc
                    if second<=gate_num_half:
                        xor_2_connection = ("out_{0}_{1}".format(parity_i, first-1), "a_{0}_{1}".format(parity_i, second-1))
                        self.xor_2_connections.append(xor_2_connection)

                    third = offset + 2*inc
                    if third<=gate_num_half:
                        xor_2_connection = ("out_{0}_{1}".format(parity_i, third-1), "b_{0}_{1}".format(parity_i, second-1))
                        self.xor_2_connections.append(xor_2_connection)
                        first_iteration = False

                    offset = offset + 4*inc

                if first_iteration and third>gate_num_half:
                    done = True
                    if second<gate_num_half:
                        xor_2_connection = ("out_{0}_{1}".format(parity_i, gate_num_half-1), "b_{0}_{1}".format(parity_i, second-1))
                        self.xor_2_connections.append(xor_2_connection)
                    
                inc = 2*inc

    def route_parity_generator(self):
        debug.info(1, "Starting routing parity generator")
        r = router.router(OPTS.openram_temp+"xor2s.gds")
        layer_stack =("metal3", "via2", "metal2")
        for connection in self.xor_2_connections:
            r.route(self, layer_stack,src=connection[0], dest=connection[1])
            #a = r.add_route(self)
        debug.info(1, "Done routing")

    def add_decoder(self):
        debug.info(1, "Starting to layout decoder logic gates")
        decoder_offset = vector(self.xor_2.width*6, 0)
        
        #place inverters
        for parity_i in range(self.parity_num):
            if parity_i%2:
                direction = "R0"
                xoffset = 0
                yoffset = parity_i*(self.inv.height)
            else:
                direction = "MX"
                xoffset = 0
                yoffset = (parity_i+1)*(self.inv.height)

            self.add_inst(name="inv",
                     mod=self.inv,
                     offset=decoder_offset+vector(xoffset, yoffset),
                     mirror=direction)
    
