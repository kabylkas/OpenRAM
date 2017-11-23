import design
import tech
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
        self.xor_2_pin_map = self.mod_xor_2.pin_map

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
        self.create_pinv()
        self.create_nand_2()
        self.setup_layout_constants()
        self.add_parity_generator()
        #self.route_parity_generator()
        #self.add_syndrome_generator()
        #self.route_syndrom_generator()
        #self.add_syndrome_to_locator_bus()
        #self.route_syndrome_to_bus()
        #self.add_locator()
        #self.route_bus_to_locator()
        #self.create_pinv()

    def create_xor_2(self):
        self.xor_2 = self.mod_xor_2("xor_2")
        self.add_mod(self.xor_2)

    def create_nand_2(self):
        self.nand_2 = nand_2(nmos_width = 2*drc["minwidth_tx"])
        self.add_mod(self.nand_2)

    def create_pinv(self):
        self.pinv = pinv(nmos_width=2*drc["minwidth_tx"],
                         height=self.xor_2.height-drc["minwidth_metal1"],
                         beta=tech.parameter["pinv_beta"])
        self.add_mod(self.pinv)

    def setup_layout_constants(self):
        #layout offsets
        self.syndrome_gen_height = self.xor_2.height
        self.syn_to_loc_bus_height = 2*self.parity_num*\
                                     (drc["minwidth_metal3"]+0.5+drc["metal3_to_metal3"])+\
                                     drc["metal3_to_metal3"]
        self.locator_height = 2*drc["metal1_to_metal1"]+\
                              2*getattr(self.nand_2, "height")
        self.global_yoffset = self.syndrome_gen_height+\
                              self.syn_to_loc_bus_height+\
                              self.locator_height
        self.current_global_yoffset = self.global_yoffset

        #module widths
        self.parity_gen_width = 0 #calculated after layout
        #reset lists
        self.vdd_positions = []
        self.gnd_positions = []
        self.a_positions = []
        self.b_positions = []
        self.out_positions = []
        self.xor_2_positions = []
        self.xor_2_connections = []
        self.parity_positions = []
        self.inv_positions = []
        self.syn_to_loc_bus_lines = []

    def add_parity_generator(self):
        debug.info(1, "Laying out xor2 gates...")
        #calculate total number of bits
        total_bit_num = self.word_size+self.parity_num

        #generate xor2 gate set for each parity bit
        global_xoffset = 0
        global_yoffset = self.current_global_yoffset

        for parity_i in range(self.parity_num):
            #calculate number of inputs for the current parity
            #refer to: http://blog.kabylkas.kz/2017/11/18/implementing-error-detecting-and-correcting-code-in-ram-how-is-it-implemented/
            #the blog post shows how number of inputs is calculated
            two_to_parity_i = int(math.pow(2, parity_i))
            check = True
            input_num = 0
            count = 0
            for bit in range(two_to_parity_i, total_bit_num+1):
                count = count + 1
                if check:
                    input_num = input_num + 1
                if count == two_to_parity_i:
                    count = 0
                    check = not check

            #subtract 1 from the calculated input number
            input_num = input_num - 1
            #number of xor2 gates=input number - 1
            gate_num = input_num-1
            #The design choice was made to split the gates in half
            #and stack them. This allows easy routing.
            #refer to: 
            #the blog post discusses the details of this design choice
            gate_num_half = int(math.floor(gate_num/2))
            for i in range(gate_num):
                name = "parity_xor2_{0}_{1}".format(parity_i, i)
                if i<gate_num_half:
                    direction = "R0"
                    xoffset = global_xoffset + i*self.xor_2.width
                    yoffset = global_yoffset
                else:
                    direction = "MX"
                    xoffset = global_xoffset + (i-gate_num_half)*self.xor_2.width
                    yoffset = global_yoffset + 2*self.xor_2.height

                a_flip_offset = vector(0,0)
                b_flip_offset = vector(0,0)
                out_flip_offset = vector(0,0)
                if direction == "MX":
                    xor_2_h = self.xor_2.height
                    ab_y_distance = self.xor_2_pin_map["a"][1]-self.xor_2_pin_map["b"][1]
                    #a
                    a_y = xor_2_h+ab_y_distance
                    a_flip_offset = vector(0,a_y)
                    #b
                    b_y = xor_2_h-ab_y_distance
                    b_flip_offset = vector(0, b_y)
                    #out
                    out_y = xor_2_h-(xor_2_h-2*self.xor_2_pin_map["out"][1])
                    out_flip_offset = vector(0, out_y)

                xor_2_position = vector(xoffset, yoffset)
                a_offset = xor_2_position+self.xor_2_pin_map["a"][0].center()-a_flip_offset
                b_offset = xor_2_position+self.xor_2_pin_map["b"][0].center()-b_flip_offset
                out_offset = xor_2_position+self.xor_2_pin_map["out"][0].center()-out_flip_offset

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

            # remember the current parity generator xoffset
            # this will be used for placement of syndrome generator
            self.parity_positions.append(global_xoffset)
            # calculate next parity generator xoffset
            global_xoffset = global_xoffset + int(math.ceil(gate_num/2))*self.xor_2.width
            if gate_num%2:
                global_xoffset = global_xoffset + self.xor_2.width

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
        
        #remember last global X offset
        self.parity_gen_width = global_xoffset
         
        #add vdd and gnd labels
        for i in range(3):
            pin_name = "gnd"
            if i%2:
                pin_name = "vdd"
            
            label_offset = vector(0,global_yoffset) + vector(0, i*self.xor_2.height)
            self.add_label(text = pin_name,
                           layer = "metal1",
                           offset = label_offset)

        #dump gds file for the router
        self.gds_write(OPTS.openram_temp+"xor2s.gds")
        
        #finish
        debug.info(1, "Done placing parity generator (xor_2 gates)...")

    def route_parity_generator(self):
        debug.info(1, "Starting routing parity generator")
        r = router.router(OPTS.openram_temp+"xor2s.gds")
        layer_stack =("metal3", "via2", "metal2")
        for connection in self.xor_2_connections:
            r.route(self, layer_stack, src=connection[0], dest=connection[1])
        debug.info(1, "Done routing parity generator")


    """
    Syndrome generator is simple set of 2 input XOR gate.
    The number of XOR gates is determened by the number of parity bits.
    The XOR gate is backed with an inverter. The inverter will be used 
    for locating the bit flip. It will be used in the next stage (decoder).
    """
    def add_syndrome_generator(self):
        debug.info(1, "Starting placement of syndrome generator")
        #get the yoffset
        global_yoffset = self.current_global_yoffset
        i=0
        for x_syndrome_position in self.parity_positions:
            ################
            #place XOR gate
            ################
            name = "syndrome_xor2_{0}".format(i)
            xor_2_position = vector(x_syndrome_position, global_yoffset)

            a_flip_offset = vector(0,0)
            b_flip_offset = vector(0,0)
            out_flip_offset = vector(0,0)
            direction = "MX"
            xor_2_h = self.xor_2.height
            ab_y_distance = self.xor_2_pin_map["a"][1]-self.xor_2_pin_map["b"][1]
            #a label
            a_y = xor_2_h+ab_y_distance
            a_flip_offset = vector(0,a_y)
            #b label
            b_y = xor_2_h-ab_y_distance
            b_flip_offset = vector(0, b_y)
            #out label
            out_y = xor_2_h-(xor_2_h-2*self.xor_2_pin_map["out"][1])
            out_flip_offset = vector(0, out_y)

            a_offset = xor_2_position+\
                       vector(self.xor_2_pin_map["a"][0], self.xor_2_pin_map["a"][1])-\
                       a_flip_offset
            b_offset = xor_2_position+\
                       vector(self.xor_2_pin_map["b"][0], self.xor_2_pin_map["b"][1])-\
                       b_flip_offset
            out_offset = xor_2_position+\
                         vector(self.xor_2_pin_map["out"][0], self.xor_2_pin_map["out"][1])-\
                         out_flip_offset

            #add current xor2 to the design
            self.add_inst(name = name, 
                          mod = self.xor_2,
                          offset = xor_2_position,
                          mirror = direction)

            self.xor_2_positions.append(xor_2_position)

            #add labels
            self.add_label(text = "syn_a_{0}".format(i),
                           layer = "metal2",
                           offset = a_offset)
            self.add_label(text = "syn_b_{0}".format(i),
                           layer = "metal2",
                           offset = b_offset)
            self.add_label(text = "syn_out_{0}".format(i),
                           layer = "metal2",
                           offset = out_offset)

            self.add_pin("syn_a_{0}".format(i))
            self.add_pin("syn_b_{0}".format(i))
            self.add_pin("syn_out_{0}".format(i))
            #connect
            self.connect_inst(["syn_a_{0}".format(i),
                               "syn_b_{0}".format(i),
                               "syn_out_{0}".format(i),
                               "vdd",
                               "gnd"])

            ######################
            #place PINV (inverter)
            ######################

            name = "syndrome_inv_{0}".format(i)
            pinv_position = vector(x_syndrome_position+self.xor_2.width, self.global_yoffset-drc["minwidth_metal1"]/2)
            #add current xor2 to the design
            self.add_inst(name = name, 
                          mod = self.pinv,
                          offset = pinv_position,
                          mirror = direction)
    
            #calculate input and output offsets
            pinv_input_position = getattr(self.pinv, "A_position")
            pinv_output_position = getattr(self.pinv, "Z_position")
  
            pinv_input_offset = pinv_position+\
                                vector(pinv_input_position[0], pinv_input_position[1])-\
                                vector(0, xor_2_h-(xor_2_h-2*pinv_input_position[1]))
            pinv_output_offset = pinv_position+\
                                 vector(pinv_output_position[0], pinv_output_position[1])-\
                                 vector(0,xor_2_h-(xor_2_h-2*pinv_output_position[1]))

            #add metal2 rect to bring the pin up
            self.add_rect(layer   = "metal2",
                          offset  = pinv_output_offset-vector(2,2),
                          width   = 4,
                          height  = 4)


            self.add_rect(layer   = "metal2",
                          offset  = pinv_input_offset-vector(0,3),
                          width   = 2,
                          height  = 4)

            #add labels/pins/connect
            self.add_label(text = "inv_a_{0}".format(i),
                           layer = "metal2",
                           offset = pinv_input_offset)
            self.add_label(text = "inv_z_{0}".format(i),
                           layer = "metal2",
                           offset = pinv_output_offset)
            self.add_pin("inv_a_{0}".format(i))
            self.add_pin("inv_z_{0}".format(i))
            self.connect_inst(["inv_a_{0}".format(i),
                               "inv_z_{0}".format(i),
                               "vdd",
                               "gnd"])

            inv_in_out_pair = [pinv_input_offset-vector(0,1), pinv_output_offset-vector(0,1)]
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[0])
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[1])
  
            #save in and out pair for routing
            self.inv_positions.append(inv_in_out_pair)
            #increase counter
            i = i + 1
        ########################
        #insert vdd and gnd rail
        ########################
        vdd_offset = vector(0,global_yoffset-self.xor_2.height-drc["minwidth_metal1"])
        self.add_rect(layer   = "metal1",
                      offset  = vdd_offset,
                      width   = self.parity_gen_width,
                      height  = 2*drc["minwidth_metal1"])
        self.add_label(text   = "vdd",
                       layer  = "metal1",
                       offset = vdd_offset)

        gnd_offset = vector(0,global_yoffset-drc["minwidth_metal1"])
        self.add_rect(layer   = "metal1",
                      offset  = gnd_offset,
                      width   = self.parity_gen_width,
                      height  = 2*drc["minwidth_metal1"])
        self.add_label(text   = "gnd",
                       layer  = "metal1",
                       offset = gnd_offset)
        #update global_y offset
        self.current_global_yoffset -= self.syndrome_gen_height

        #finish
        debug.info(1, "Done syndrom layout")
        
    def add_syndrome_to_locator_bus(self):
        debug.info(1, "Starting to layout syndrome to locator bus")
        m2m = drc["metal3_to_metal3"]+0.5
        m_min = drc["minwidth_metal3"]
        global_yoffset = self.current_global_yoffset-m2m
        j=0
        for i in range(2*self.parity_num):
            global_yoffset -= (m2m+m_min)
            line_offset = vector(0, global_yoffset)
            self.add_rect(layer   = "metal3",
                          offset  = line_offset,
                          width   = self.parity_gen_width,
                          height  = m_min)
            line_label = "s_out_{0}".format(j)
            if i%2:
                line_label = "s_out_{0}_not".format(j)
                j+=1

            self.add_label(text   = line_label,
                           layer  = "metal3",
                           offset = line_offset+vector(1,1))
            self.add_pin(line_label)
            self.syn_to_loc_bus_lines.append(global_yoffset)
        
        #update global_yoffset
        self.current_global_yoffset -= self.syn_to_loc_bus_height

        #finish
        debug.info(1, "Done syndrome to locator bus layout")

    def route_syndrome_to_bus(self):
        debug.info(1, "Starting to route syndrome to locator bus")
        m2m = drc["metal2_to_metal2"]
        m2min = drc["minwidth_metal3"]
        i = 0
        for inv_pos in self.inv_positions:
            in_offset = inv_pos[0]
            out_offset = inv_pos[1]
            in_v_line_offset = vector(in_offset[0], self.syn_to_loc_bus_lines[i])
            out_v_line_offset = vector(out_offset[0], self.syn_to_loc_bus_lines[i+1])
            in_height = in_offset[1]-self.syn_to_loc_bus_lines[i]
            out_height = out_offset[1]-self.syn_to_loc_bus_lines[i+1]

            self.add_rect(layer   = "metal2",
                          offset  = in_v_line_offset,
                          width   = m2min,
                          height  = in_height)

            self.add_rect(layer   = "metal2",
                          offset  = out_v_line_offset,
                          width   = m2min,
                          height  = out_height)

            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = in_v_line_offset)

            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = out_v_line_offset)

            i += 2
        debug.info(1, "Done syndrome to locator bus route")
        
    """
    Locator is the module that locates the bit flip. Locator is made of NAND gates
    """
    def add_locator(self):
        debug.info(1, "Starting to layout locator logic gates")
        global_yoffset = self.current_global_yoffset
        global_yoffset -= (1.5*drc["metal1_to_metal1"]+getattr(self.nand_2, "height"))
        #place NAND gates
        gate_num = self.parity_num-1
        gate_num_half = int(gate_num/2)
        if gate_num%2:
            gate_num_half = int(gate_num/2)+1
        global_xoffset=0
        nand_2_width = getattr(self.nand_2, "width")
        nand_2_height = getattr(self.nand_2, "height")
        additional_offset = (self.parity_gen_width-self.word_size*gate_num_half*nand_2_width)/(self.word_size*gate_num_half)
        for i in range(self.word_size):
            for j in range(gate_num):
                name = "locator_nand_{0}_{1}".format(i,j)
                xoffset = 0
                flip = 0
                if j<gate_num_half:
                    xoffset = j*(nand_2_width+additional_offset)
                    direction = "R0"
                else:
                    xoffset = (j-gate_num_half)*(nand_2_width+additional_offset)
                    direction = "MX"
                    flip = 1
                xoffset += global_xoffset
                nand_2_position = vector(xoffset, global_yoffset)
                #add current xor2 to the design
                self.add_inst(name = name, 
                              mod = self.nand_2,
                              offset = nand_2_position,
                              mirror = direction)
        
                #calculate input and output offsets
                nand_2_a_position = getattr(self.nand_2, "A_position")
                nand_2_b_position = getattr(self.nand_2, "B_position")
                nand_2_z_position = getattr(self.nand_2, "Z_position")
      
                nand_2_a_offset = nand_2_position+\
                                  vector(nand_2_a_position[0], nand_2_a_position[1])-\
                                  vector(0, flip*(nand_2_height-(nand_2_height-2*nand_2_a_position[1])))
                nand_2_b_offset = nand_2_position+\
                                  vector(nand_2_b_position[0], nand_2_b_position[1])-\
                                  vector(0, flip*(nand_2_height-(nand_2_height-2*nand_2_b_position[1])))
                nand_2_z_offset = nand_2_position+\
                                  vector(nand_2_z_position[0], nand_2_z_position[1])-\
                                  vector(0, flip*(nand_2_height-(nand_2_height-2*nand_2_z_position[1])))

                #add metal2 rect to bring the pin up
                self.add_rect(layer   = "metal2", 
                              offset  = nand_2_a_offset-vector(2,flip*3),
                              width   = 3,
                              height  = 3)
                self.add_rect(layer   = "metal2", 
                              offset  = nand_2_b_offset-vector(2,flip*3),
                              width   = 3,
                              height  = 3)
                self.add_rect(layer   = "metal2", 
                              offset  = nand_2_z_offset-vector(0, flip*3),
                              width   = 3,
                              height  = 3)

                #add labels/pins/connect
                self.add_label(text = "nand2_a_{0}_{1}".format(i,j),
                               layer = "metal2",
                               offset = nand_2_a_offset+vector(-1,1-2*flip))
                self.add_label(text = "nand2_b_{0}_{1}".format(i,j),
                               layer = "metal2",
                               offset = nand_2_b_offset+vector(-1,1-2*flip))
                self.add_label(text = "nand2_z_{0}_{1}".format(i,j),
                               layer = "metal2",
                               offset = nand_2_z_offset+vector(1,1-2*flip))

                self.add_pin("nand_2_a_{0}_{1}".format(i,j))
                self.add_pin("nand_2_b_{0}_{1}".format(i,j))
                self.add_pin("nand_2_z_{0}_{1}".format(i,j))
                self.connect_inst(["nand_2_a_{0}_{1}".format(i,j),
                                   "nand_2_b_{0}_{1}".format(i,j),
                                   "nand_2_z_{0}_{1}".format(i,j),
                                   "vdd",
                                   "gnd"])
                
                self.add_via(layers   = ("metal1", "via1", "metal2"),
                             offset   = nand_2_a_offset-vector(0, flip))
                self.add_via(layers   = ("metal1", "via1", "metal2"),
                             offset   = nand_2_b_offset-vector(2,flip))
                self.add_via(layers   = ("metal1", "via1", "metal2"),
                             offset   = nand_2_z_offset-vector(0, flip))
            global_xoffset+=gate_num_half*(nand_2_width+additional_offset)
        
        #add vdd and gnd rails
        gnd_offset = vector(0,global_yoffset-drc["minwidth_metal1"]/2)
        self.add_rect(layer   = "metal1",
                      offset  = gnd_offset,
                      width   = self.parity_gen_width,
                      height  = drc["minwidth_metal1"])
        self.add_label(text = "gnd",
                       layer = "metal1",
                       offset = gnd_offset)
        #upper vdd
        vdd_up_offset = gnd_offset + vector(0, nand_2_height)
        self.add_rect(layer   = "metal1",
                      offset  = vdd_up_offset,
                      width   = self.parity_gen_width,
                      height  = drc["minwidth_metal1"])
        self.add_label(text = "vdd",
                       layer = "metal1",
                       offset = vdd_up_offset)
        #bottom vdd
        vdd_down_offset = gnd_offset - vector(0, nand_2_height)
        self.add_rect(layer   = "metal1",
                      offset  = vdd_down_offset,
                      width   = self.parity_gen_width,
                      height  = drc["minwidth_metal1"])
        self.add_label(text = "vdd",
                       layer = "metal1",
                       offset = vdd_down_offset)
        #dump gds for routing
        self.gds_write(OPTS.openram_temp+"locator.gds")
        #finish
        debug.info(1, "Done locator logic gates layout")
    
    def route_bus_to_locator(self):
        debug.info(1, "Starting to route bus to locator")
        connections = []
        connections.append(["nand2_a_0_0", "s_out_3"])
        connections.append(["nand2_b_0_0", "s_out_2_not"])
        connections.append(["nand2_a_0_1", "s_out_1_not"])
        connections.append(["nand2_b_0_1", "s_out_3"])

        r = router.router(OPTS.openram_temp+"locator.gds")
        layer_stack =("metal3", "via2", "metal2")
        for connection in connections:
            r.route(self, layer_stack,src=connection[0], dest=connection[1])
        
        debug.info(1, "Done bus to locator route")
