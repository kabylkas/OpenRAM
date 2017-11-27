"""
Links/Refences:
(1) http://blog.kabylkas.kz/2017/11/18/implementing-error-detecting-and-correcting-code-in-ram-how-is-it-implemented/
(2) {POST ABOUT STACKING}
"""
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
        for pin in self.mod_xor_2.pin_map:
          print(pin)
        self.word_size = word_size
        self.parity_num = int(math.floor(math.log(word_size,2)))+1;

        self.add_pins()
        self.create_layout()
        #self.print_drc_rules()
        #self.DRC_LVS()

    def print_drc_rules(self):
        for key, value in drc.iteritems():
            print key, value

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
        #self.generate_parity_connections()
        #self.route_parity_generator()
        #self.add_syndrome_generator()
        #self.route_syndrome_generator()
        #self.add_syndrome_to_locator_bus()
        #self.add_locator()
        #self.route_bus_to_locator()
        #self.route_bus_to_syndrome()
        #self.route_locator()
        #self.add_corrector()
        #self.route_corrector()

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
                                     (drc["minwidth_metal1"]+drc["metal1_enclosure_via1"]+drc["metal1_to_metal1"])+\
                                     drc["metal1_to_metal1"]
        self.locator_height = 2*drc["metal1_to_metal1"]+\
                              2*getattr(self.nand_2, "height")
        self.corrector_height = self.xor_2.height+getattr(self.pinv, "height")
        self.global_yoffset = self.syndrome_gen_height+\
                              self.syn_to_loc_bus_height+\
                              self.locator_height+\
                              self.corrector_height
        self.current_global_yoffset = self.global_yoffset

        #module widths
        self.parity_gen_width = 0 #calculated after layout
        #init lists
        self.vdd_positions = []
        self.gnd_positions = []
        self.xor_2_positions = []
        self.xor_2_label_positions = {}
        self.parity_output_gates = []
        self.locator_output_gate = 0
        self.syn_label_positions = {}
        self.cor_label_positions = {}
        self.xor_2_up_connections = []
        self.xor_2_down_connections = []
        self.parity_positions = []
        self.locator_positions = {}
        self.nand_2_up_connections = []
        self.nand_2_down_connections = []
        self.inv_positions = []
        self.syn_to_loc_bus_lines = []
        self.syn_to_loc_bus_line_positions = {}

    def mirror_xor_2(self):
        direction="MX"
        self.xor_2_direction = direction
        self.xor_2_pin_map["a"][0].transform(0, direction, 0)
        self.xor_2_pin_map["b"][0].transform(0, direction, 0)
        self.xor_2_pin_map["out"][0].transform(0, direction, 0)
        return self.get_xor_2_pin_pos()
        
    def get_xor_2_pin_pos(self):
        a_pos = self.xor_2_pin_map["a"][0].center()
        b_pos = self.xor_2_pin_map["b"][0].center()
        out_pos = self.xor_2_pin_map["out"][0].center()
        return a_pos, b_pos, out_pos
        
    """
    Generic function to add arbitrary module into design
    """
    def add_to_design(self, mod_name, pin_name, mod, index, position, direction, offset, skip=["vdd", "gnd"]):
        name = mod_name+"_{0}_{1}".format(parity_i, i)

        #add module
        self.add_inst(name = name, 
                      mod = mod,
                      offset = positions,
                      mirror = direction)

        for pin in mod.pin_map:
        #add labels
        self.add_label(text = "_a_{0}_{1}".format(parity_i, i),
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


    """
    Parity generator is the interconnection of xor2 gates that calculate the parity.
    Refer to link (1) shown at the top of this file.
    The blog post discusses what is parity and the chosen algoritm
    """  
    def add_parity_generator(self):
        debug.info(1, "Laying out xor2 gates...")
        #calculate total number of bits
        total_bit_num = self.word_size+self.parity_num

        #generate xor2 gate set for each parity bit
        global_xoffset = 0
        global_yoffset = self.current_global_yoffset

        a_pos, b_pos, out_pos = self.get_xor_2_pin_pos()

        #start laying out
        for parity_i in range(self.parity_num):
            #calculate number of inputs for the current parity
            #refer to the link (1). 
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
            self.gate_num = gate_num
            #The design choice was made to split the gates in half
            #and stack them. This allows easy routing.
            #refer to: {BLOG_ABOUT STACKING XOR} 
            #the blog post discusses the details of this design choice
            gate_num_half = int(math.floor(gate_num/2))
            self.xor_2_direction="R0"
            for i in range(gate_num):
                if i<gate_num_half:
                    xoffset = global_xoffset + i*self.xor_2.width
                    yoffset = global_yoffset
                else:
                    xoffset = global_xoffset + (i-gate_num_half)*self.xor_2.width
                    yoffset = global_yoffset + 2*self.xor_2.height

                #mirror the pins as we pass to the second half of gate 
                if i==gate_num_half:
                    #mirror and update pin positions
                    a_pos, b_pos, out_pos = self.mirror_xor_2()

                #calculate position for the current gate
                xor_2_position = vector(xoffset, yoffset)
                a_offset = xor_2_position+a_pos
                b_offset = xor_2_position+b_pos
                out_offset = xor_2_position+out_pos

                #add to the design
                self.add_to_design("parity_xor_2", "par",  parity_i, i, xor_2_position, a_offset, b_offset, out_offset)

                #save for routing
                self.xor_2_label_positions["a_{0}_{1}".format(parity_i, i)] = a_offset
                self.xor_2_label_positions["b_{0}_{1}".format(parity_i, i)] = b_offset
                self.xor_2_label_positions["out_{0}_{1}".format(parity_i, i)] = out_offset
                self.xor_2_positions.append(xor_2_position)        
                
            #mirror back before laying out gates for next parity 
            a_pos, b_pos, out_pos = self.mirror_xor_2()

            # remember the current parity generator xoffset
            # this will be used for placement of syndrome generator
            self.parity_positions.append(global_xoffset)

            # calculate next parity generator xoffset
            global_xoffset = global_xoffset + int(math.ceil(gate_num/2))*self.xor_2.width
            if gate_num%2:
                global_xoffset = global_xoffset + self.xor_2.width

         
        #add vdd and gnd labels for pairty generator
        for i in range(3):
            pin_name = "gnd"
            if i%2:
                pin_name = "vdd"
            
            label_offset = vector(0,global_yoffset) + vector(0, i*self.xor_2.height)
            self.add_label(text = pin_name,
                           layer = "metal1",
                           offset = label_offset)

        #remember last global X offset
        self.parity_gen_width = global_xoffset
        
        #finish
        debug.info(1, "Done placing parity generator (xor_2 gates)...")


    """
    After the xor gates that generate parity were laid out, this function
    generates all required connection between xor gates that will be used 
    by routing function (next function). The generation of the connections
    are based on our design choise to stack the xor gates in two rows. This
    allows routing with now metal overlap. Refer to link (2).
    This function only figures out the pairs to connect. It does not involve
    any layout or actual routing.
    """
    def generate_parity_connections(self):
        debug.info(1, "Generating connections for router...")
        total_bit_num = self.word_size+self.parity_num

        for parity_i in range(self.parity_num):
            #calculate number of inputs for the current parity
            #refer to the link (1). 
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
            gate_num_half = int(math.floor(gate_num/2))
            #1. generate connections between xor gates in the upper row 
            dst = 0
            src = gate_num_half
            while dst<gate_num_half:
                xor_2_connection = ("out_{0}_{1}".format(parity_i, src), "a_{0}_{1}".format(parity_i, dst))
                self.xor_2_up_connections.append(xor_2_connection)
                if src+1<gate_num:
                    xor_2_connection = ("out_{0}_{1}".format(parity_i, src+1), "b_{0}_{1}".format(parity_i, dst))
                    self.xor_2_up_connections.append(xor_2_connection)
                dst=dst+2
                src=src+2
            #add one more connection if upper row gates are not even
            if gate_num%2:
                up_row_gate_num = gate_num-gate_num_half
                if up_row_gate_num%2:
                    xor_2_connection = ("out_{0}_{1}".format(parity_i,gate_num-1), "b_{0}_{1}".format(parity_i, gate_num_half-1))
                    self.xor_2_up_connections.append(xor_2_connection)

            #2.generate connections between xor gates in the bottom row
            inc = 1
            done = False
            depth = 0
            out = 0
            while not done:
                offset = inc
                first_iteration = True
                while offset<=gate_num_half:
                    first = offset
                    second = offset + inc
                    if second<=gate_num_half:
                        xor_2_connection = ("out_{0}_{1}".format(parity_i, first-1), "a_{0}_{1}".format(parity_i, second-1), depth)
                        print(xor_2_connection)
                        self.xor_2_down_connections.append(xor_2_connection)
                        out = second-1

                    third = offset + 2*inc
                    if third<=gate_num_half:
                        xor_2_connection = ("b_{0}_{1}".format(parity_i, second-1), "out_{0}_{1}".format(parity_i, third-1), depth)
                        self.xor_2_down_connections.append(xor_2_connection)
                        first_iteration = False
                        out = second-1

                    offset = offset + 4*inc

                if first_iteration and third>gate_num_half:
                    done = True
                    if second<gate_num_half:
                        xor_2_connection = ("b_{0}_{1}".format(parity_i, second-1), "out_{0}_{1}".format(parity_i, gate_num_half-1), depth)
                        self.xor_2_down_connections.append(xor_2_connection)
                        out = second-1
                    
                inc = 2*inc
                depth += 1
            self.parity_output_gates.append(out)

        #finish
        debug.info(1, "Done generating connections for router...")

    """
    Router of the parity generator. This router makes use of the patterns
    in the parity generator layout, and routes the pins as discussed in 
    link (2).
    The routing is performed based on the connections generated by
    generate_parity_connections() function.
    """
    def route_parity_generator(self):
        debug.info(1, "Starting routing parity generator")
        #route upper row of xor gates
        m2min = drc["minwidth_metal2"]
        m3min = drc["minwidth_metal3"]
        m2m = drc["metal2_to_metal2"]
        m3m = drc["metal3_to_metal3"]
        m3_extend_via2 = drc["metal3_extend_via2"] 
        for connection in self.xor_2_up_connections:
            src = self.xor_2_label_positions[connection[0]]
            dest = self.xor_2_label_positions[connection[1]]
            yoffset = self.xor_2_label_positions["a_0_0"][1] + (m3m+m3min)
            #vertical m2 from source up to yoffset
            w = m2m
            h = src[1]-yoffset
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #vertical m2 from destination up to yoffset
            w = m2m
            h = yoffset-dest[1]
            offset = vector(dest[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #horizontal m3 from src to destination on yoffset
            w = dest[0]-src[0]
            h = m3min
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal3",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #add vias on both ends
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))

        for connection in self.xor_2_down_connections:
            src = self.xor_2_label_positions[connection[0]]
            dest = self.xor_2_label_positions[connection[1]]
            depth = connection[2]
            m2min = drc["minwidth_metal2"]
            m3m = drc["metal3_to_metal3"]
            m3min = drc["minwidth_metal3"]
            yoffset = self.xor_2_label_positions["out_0_0"][1] - m3m-m3min - depth*(m3m+m3min)

            m3_offset = vector(src[0], yoffset)-vector(m2min,0)
            w = dest[0]-src[0]
            self.add_rect(layer   = "metal3",
                          offset  = m3_offset,
                          width   = w,
                          height  = drc["minwidth_metal3"])

            m2_offset = m3_offset
            w = m2min
            h = src[1]-yoffset
            self.add_rect(layer   = "metal2",
                          offset  = m2_offset,
                          width   = w,
                          height  = h)
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = m2_offset)

            m2_offset = vector(dest[0], yoffset)-vector(m2min,0)
            w = m2min
            h = dest[1]-yoffset
            self.add_rect(layer   = "metal2",
                          offset  = m2_offset,
                          width   = w,
                          height  = h)
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = m2_offset)

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
            if (self.word_size>=16):
                xor_2_position = vector(self.xor_2_label_positions["out_{0}_{1}".format(i,self.parity_output_gates[i])][0],global_yoffset)-\
                                 vector(self.xor_2_label_positions["b_0_0"][0],0)
            else:
                xor_2_position = vector(x_syndrome_position, global_yoffset)


            a_pos, b_pos, out_pos = self.mirror_xor_2()

            a_offset = xor_2_position+a_pos
            b_offset = xor_2_position+b_pos
            out_offset = xor_2_position+out_pos

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

            #remember label positions for routing
            self.syn_label_positions["syn_a_{0}".format(i)] = a_offset
            self.syn_label_positions["syn_b_{0}".format(i)] = b_offset
            self.syn_label_positions["syn_out_{0}".format(i)] = out_offset
            #add pins
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
            if (self.word_size>=16):
                pinv_position = vector(self.xor_2_label_positions["out_{0}_{1}".format(i,self.parity_output_gates[i])][0],0)+\
                                vector(self.xor_2.width+2*drc["metal2_to_metal2"], self.global_yoffset-drc["minwidth_metal1"]/2)-\
                                vector(self.xor_2_label_positions["b_0_0"][0],0)
            else:
                pinv_position = vector(x_syndrome_position+self.xor_2.width+2*drc["metal2_to_metal2"], self.global_yoffset-drc["minwidth_metal1"]/2)
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
        
            minm1 = drc["minwidth_metal1"]
            inv_in_out_pair = [pinv_input_offset-vector(0,minm1), pinv_output_offset-vector(0,minm1)]
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[0])
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[1])
  
            #save in and out pair for routing
            self.inv_positions.append(inv_in_out_pair)
            #remember label offsets for routing
            self.syn_label_positions["inv_a_{0}".format(i)] = inv_in_out_pair[0]
            self.syn_label_positions["inv_z_{0}".format(i)] = inv_in_out_pair[1]
            
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
        
    def route_syndrome_generator(self):
        debug.info(1, "Starting to route syndrome generator")
        #route syndrome output to the inverter
        for i in range(self.parity_num):
            connection = ("syn_out_{0}".format(i), "inv_a_{0}".format(i))

            src = self.syn_label_positions[connection[0]]
            dest = self.syn_label_positions[connection[1]]
            m2min = drc["minwidth_metal2"]
            m3min = drc["minwidth_metal3"]
            m2m = drc["metal2_to_metal2"]
            m3m = drc["metal3_to_metal3"]
            yoffset = src[1]+m3m+m3min
            m3_extend_via2 = drc["metal3_extend_via2"] 
            #vertical m2 from source up to yoffset
            w = m2m
            h = yoffset-src[1]
            offset = vector(src[0], src[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #vertical m2 from destination up to yoffset
            w = m2m
            h = yoffset-dest[1]
            offset = vector(dest[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #horizontal m3 from src to destination on yoffset
            w = dest[0]-src[0]
            h = m3min
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal3",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #add vias on both ends
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))

        #route parity outputs to the syndrome generator
        i=0
        for out_gate in self.parity_output_gates:
            connection = ("out_{0}_{1}".format(i, out_gate), "syn_b_{0}".format(i))
            i+=1
            src = self.xor_2_label_positions[connection[0]]
            dest = self.syn_label_positions[connection[1]]
            m2min = drc["minwidth_metal2"]
            m3min = drc["minwidth_metal3"]
            m2m = drc["metal2_to_metal2"]
            m3m = drc["metal3_to_metal3"]
            m3_extend_via2 = drc["metal3_extend_via2"]
            yoffset = dest[1]+6*(m3m+m3min)
            #vertical m2 from source down to yoffset
            w = m2m
            h = src[1]-yoffset
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #vertical m2 from source up to yoffset
            w = m2m
            h = dest[1]-yoffset
            offset = vector(dest[0], yoffset)
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #horizontal m3 from src to destination on yoffset
            w = dest[0]-src[0]
            h = m3min
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal3",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #add vias on both ends
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
        #finish
        debug.info(1, "Done syndrom generator route")

    def add_syndrome_to_locator_bus(self):
        debug.info(1, "Starting to layout syndrome to locator bus")
        m1m = drc["metal1_to_metal1"]
        m_min = drc["minwidth_metal1"]+drc["metal1_enclosure_via1"]
        global_yoffset = self.current_global_yoffset-m1m
        j=0
        for i in range(2*self.parity_num):
            global_yoffset -= (m1m+m_min)
            line_offset = vector(0, global_yoffset)
            self.add_rect(layer   = "metal1",
                          offset  = line_offset,
                          width   = self.parity_gen_width+5*m_min,
                          height  = m_min)
            line_label = "s_out_{0}".format(j)
            if i%2:
                line_label = "s_out_{0}_not".format(j)
                j+=1

            self.add_label(text   = line_label,
                           layer  = "metal1",
                           offset = line_offset+vector(1,1))
            self.add_pin(line_label)
            self.syn_to_loc_bus_lines.append(global_yoffset)
            self.syn_to_loc_bus_line_positions[line_label] = global_yoffset
        #update global_yoffset
        self.current_global_yoffset -= self.syn_to_loc_bus_height

        #finish
        debug.info(1, "Done syndrome to locator bus layout")

        
    """
    Locator is the module that locates the bit flip. Locator is made of NAND gates.
    The number of NAND gates determined by the number of parity bits and the word width.
    Example: ECC for 16 bit word size requires 5 parity bits. Locator for 5 parity bits
    requires 4 2-input NAND gates for each of the 16 bits. Thus number of NAND gates if 4*16
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

                #append labels to connections as destination, source will be added later
                if direction == "R0":
                    self.syn_to_loc_bus_connections.append(["", "nand_2_a_{0}_{1}".format(i,j)])
                    self.syn_to_loc_bus_connections.append(["", "nand_2_b_{0}_{1}".format(i,j)])

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
                             offset   = nand_2_b_offset-vector(0,flip))
                self.add_via(layers   = ("metal1", "via1", "metal2"),
                             offset   = nand_2_z_offset-vector(0, flip))
                if flip:
                    self.add_via(layers   = ("metal1", "via1", "metal2"),
                                 offset   = nand_2_b_offset-vector(flip*2*drc["minwidth_metal3"], flip))
                

                self.locator_positions["nand_2_a_{0}_{1}".format(i,j)] = nand_2_a_offset-vector(0, flip)
                self.locator_positions["nand_2_b_{0}_{1}".format(i,j)] = nand_2_b_offset-vector(flip*2*drc["minwidth_metal3"], flip)
                self.locator_positions["nand_2_z_{0}_{1}".format(i,j)] = nand_2_z_offset-vector(0, flip)
            global_xoffset+=gate_num_half*(nand_2_width+additional_offset)
            #adding last connection from syndrome to locator bus in case 
            #gate numbers on upper row are even 
            if not gate_num%2:
                self.syn_to_loc_bus_connections.append(["", "nand_2_b_{0}_{1}".format(i,gate_num-1)])
            
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

        #generate source of the connections between bus and the locator
        total_bit_num = self.word_size+self.parity_num
        k=0
        for i in range(1,total_bit_num+1):
            log2 = math.log10(i)/math.log10(2)
            if not (log2-math.ceil(log2))==0:
                number = i
                for j in range(self.parity_num):
                    src = ""
                    if number%2:
                        src = "s_out_{0}".format(j)
                    else:
                        src = "s_out_{0}_not".format(j)
                    self.syn_to_loc_bus_connections[k][0] = src
                    number = number >> 1
                    k+=1

        self.current_global_yoffset-=self.locator_height+getattr(self.pinv, "height")
        #finish
        debug.info(1, "Done locator logic gates layout")

    def route_locator(self):
        debug.info(1, "Starting to route locator")
        #generate inter NAND connection with in the locator
        #generate connections between xor gates in the upper row to down row xor gates
        gate_num = self.parity_num-1
        gate_num_half=int(gate_num/2)
        if gate_num%2:
            gate_num_half+=1

        dst = gate_num_half
        src = 0
        while dst<gate_num:
            nand_2_connection = ("z_{0}".format(src), "a_{0}".format(dst))
            self.nand_2_up_connections.append(nand_2_connection)
            if src+1<gate_num_half:
                nand_2_connection = ("z_{0}".format(src+1), "b_{0}".format(dst))
                self.nand_2_up_connections.append(nand_2_connection)
            dst=dst+2
            src=src+2
        #add one more connection if upper row gates are not even
        if gate_num%2:
            up_row_gate_num = gate_num-gate_num_half+1
            print up_row_gate_num
            if up_row_gate_num%2:
                nand_2_connection = ("z_{0}".format(gate_num_half-1), "b_{0}".format(gate_num-1))
                self.nand_2_up_connections.append(nand_2_connection)

        #generate connections between nand gates in the bottom row
        inc = 1
        done = False
        depth = 0
        out = gate_num-1
        minus = 1
        if gate_num%2:
            gate_num_half-=1
            minus = 0
        while not done:
            offset = inc
            first_iteration = True
            while offset<=gate_num_half:
                first = offset
                second = offset + inc
                if second<=gate_num_half:
                    nand_2_connection = ("z_{0}".format(first+gate_num_half-1*minus), 
                                         "a_{0}".format(second+gate_num_half-1*minus), 
                                         depth)
                    self.nand_2_down_connections.append(nand_2_connection)
                    out = second+gate_num_half-1*minus

                third = offset + 2*inc
                if third<=gate_num_half:
                    nand_2_connection = ("b_{0}".format(second+gate_num_half-1*minus), 
                                         "z_{0}".format(third+gate_num_half-1*minus), 
                                         depth)
                    self.nand_2_down_connections.append(nand_2_connection)
                    first_iteration = False
                    out = second+gate_num_half-1*minus

                offset = offset + 4*inc

            if first_iteration and third>gate_num_half:
                done = True
                if second<gate_num_half:
                    nand_2_connection = ("b_{0}".format(second+gate_num_half-1*minus), 
                                         "z_{0}".format(gate_num_half+gate_num_half-1*minus),
                                         depth)
                    self.nand_2_down_connections.append(nand_2_connection)
                    out = second+gate_num_half-1*minus
            
            self.locator_output_gate = out
            inc = 2*inc
            depth += 1

        #route the NAND gates according to the generated connections above
        m2m = drc["metal2_to_metal2"]
        m2min = drc["minwidth_metal2"]
        m3m = drc["metal3_to_metal3"]
        m3min = drc["minwidth_metal3"]
        m3_extend_via2 = drc["metal3_extend_via2"]
        a_y = 0
        first = True
        for i in range(self.word_size):
            k = 0
            #route upper NAND gates
            for connection in self.nand_2_up_connections:
                k+=1
                #get source pin and reformat it
                src_label = connection[0]
                temp = src_label.split("_")
                src_label = "nand_2_{0}_{1}_{2}".format(temp[0], i, temp[1])
                src = self.locator_positions[src_label]
                #get destination pin and reformat it
                dest_label = connection[1]
                temp = dest_label.split("_")
                dest_label = "nand_2_{0}_{1}_{2}".format(temp[0], i, temp[1])
                dest = self.locator_positions[dest_label]
                #define bend y position
                if k%2:
                    yoffset = src[1]-3*m3m
                else:
                    yoffset = src[1]-3*(m3m+m3min)
                    dest[0] = dest[0] + 2*drc["minwidth_metal3"]
                #vertical m2 from source down to yoffset
                w = m2m
                h = src[1]-yoffset
                offset = vector(src[0], yoffset)
                self.add_rect(layer   = "metal2",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #vertical m2 from source up to yoffset
                w = m2m
                h = yoffset-dest[1]
                offset = vector(dest[0], dest[1]) 
                self.add_rect(layer   = "metal2",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #horizontal m3 from src to destination on yoffset
                w = src[0]-dest[0]
                h = m3min
                offset = vector(dest[0], yoffset)
                self.add_rect(layer   = "metal3",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #add vias on both ends
                self.add_via(layers   = ("metal3", "via2", "metal2"),
                             offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
                self.add_via(layers   = ("metal3", "via2", "metal2"),
                             offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))

            k=0
            for connection in self.nand_2_down_connections:
                k+=1
                #get source pin and reformat it
                src_label = connection[0]
                temp = src_label.split("_")
                src_label = "nand_2_{0}_{1}_{2}".format(temp[0], i, temp[1])
                src = self.locator_positions[src_label]
                #get destination pin and reformat it
                dest_label = connection[1]
                temp = dest_label.split("_")
                dest_label = "nand_2_{0}_{1}_{2}".format(temp[0], i, temp[1])
                dest = self.locator_positions[dest_label]
                #get the depth of the connection
                depth = connection[2]
                if first:
                    first = False
                    a_y = dest[1]
                if k%2:
                    yoffset = a_y-(1+depth)*(m3m+m3min)
                else:
                    yoffset = a_y-(2+depth)*(2*m3m+m3min)
                    
                #vertical m2 from source down to yoffset
                w = m2m
                h = src[1]-yoffset
                offset = vector(src[0], yoffset)
                self.add_rect(layer   = "metal2",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #vertical m2 from source up to yoffset
                w = m2m
                h = dest[1]-yoffset
                offset = vector(dest[0], yoffset) 
                self.add_rect(layer   = "metal2",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #horizontal m3 from src to destination on yoffset
                w = dest[0]-src[0]
                h = m3min
                offset = vector(src[0], yoffset)
                self.add_rect(layer   = "metal3",
                              offset  = offset,
                              width   = w,
                              height  = h)
                #add vias on both ends
                self.add_via(layers   = ("metal3", "via2", "metal2"),
                             offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
                self.add_via(layers   = ("metal3", "via2", "metal2"),
                             offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))

        #finish        
        debug.info(1, "Done locator")
      
    def route_bus_to_locator(self):
        debug.info(1, "Starting to route bus to locator")
        for connection in self.syn_to_loc_bus_connections:
            src = self.syn_to_loc_bus_line_positions[connection[0]]
            dest = self.locator_positions[connection[1]]
            m2min = drc["minwidth_metal2"]
            m3min = drc["minwidth_metal3"]
            m2m = drc["metal2_to_metal2"]
            m3m = drc["metal3_to_metal3"]
            m3_extend_via2 = drc["metal3_extend_via2"]
            #vertical m2 from source down to yoffset
            w = m2m
            h = src-dest[1]
            offset = vector(dest[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = vector(dest[0], src))
             
        #finish 
        debug.info(1, "Done bus to locator route")

    def route_bus_to_syndrome(self):
        debug.info(1, "Starting to route syndrome to locator bus")
        m2m = drc["metal2_to_metal2"]
        m2min = drc["minwidth_metal2"]
        m3m = drc["metal3_to_metal3"]
        m3min = drc["minwidth_metal3"]
        m3_extend_via2 = drc["metal3_extend_via2"]
        required_m2m = 2*(m2m+m2min)
        i = 0
        bend = False
        #sort connections
        locator_input_x_positions = []
        for connection in self.syn_to_loc_bus_connections:
            nand2_input_positions = self.locator_positions[connection[1]]
            xoffset = nand2_input_positions[0]
            locator_input_x_positions.append(xoffset)
        locator_input_x_positions.append(self.parity_gen_width) 
        for inv_pin_positions in self.inv_positions:
            for inv_pin in inv_pin_positions:
                locator_input_x_positions.sort()
                in_offset = inv_pin
                xoffset1 = 0
                xoffset2 = 0
                first = True
                bend = False
                
                for k in range(len(locator_input_x_positions)):
                    xoffset2 = locator_input_x_positions[k]
                    if xoffset1>in_offset[0]:
                        break
                    if not first:
                        if xoffset1 < in_offset[0] and in_offset[0] < xoffset2:
                            print xoffset1, in_offset[0], xoffset2
                            if in_offset[0]-xoffset1<required_m2m or xoffset2-in_offset[0]<=required_m2m:
                                bend = True
                                kk = 0
                                mid_point = xoffset1+(xoffset2-xoffset1)/2
                                while in_offset[0]-xoffset1<required_m2m and\
                                      xoffset2-in_offset[0]<required_m2m:
                                    kk+=1
                                    if k+kk==len(locator_input_x_positions):
                                       debug.info(1, "Problems with routing, potential DRC violation") 
                                       break
                                    xoffset1 = xoffset2
                                    xoffset2 = locator_input_x_positions[k+kk]
                    first = False
                    if bend:
                        break
                    xoffset1 = xoffset2
                
                if bend:
                    mid_point = xoffset1+(xoffset2-xoffset1)/2
                    locator_input_x_positions.append(mid_point)
                    print mid_point
                    yoffset = in_offset[1]-4*(m3m+m3min)
                    #vertical m2 from source down to yoffset
                    w = m2m
                    h = in_offset[1]-yoffset
                    offset = vector(in_offset[0], yoffset)
                    self.add_rect(layer   = "metal2",
                                  offset  = offset,
                                  width   = w,
                                  height  = h)
                    #vertical m2 from source up to yoffset
                    w = m2m
                    h = yoffset-self.syn_to_loc_bus_lines[i]+m2m
                    offset = vector(mid_point, self.syn_to_loc_bus_lines[i])
                    self.add_rect(layer   = "metal2",
                                  offset  = offset,
                                  width   = w,
                                  height  = h)
                    #horizontal m3 from src to destination on yoffset
                    w = in_offset[0]-mid_point+m2m
                    h = m2min
                    offset = vector(mid_point, yoffset)
                    self.add_rect(layer   = "metal2",
                                  offset  = offset,
                                  width   = w,
                                  height  = h)
                    #add vias on both ends
                    self.add_via(layers   = ("metal1", "via1", "metal2"),
                                 offset   = vector(mid_point, self.syn_to_loc_bus_lines[i]))
                else:
                    in_height = in_offset[1]-self.syn_to_loc_bus_lines[i]
                    in_v_line_offset = vector(in_offset[0], self.syn_to_loc_bus_lines[i])
                    self.add_rect(layer   = "metal2",
                                  offset  = in_v_line_offset,
                                  width   = m2min,
                                  height  = in_height)
                    self.add_via(layers   = ("metal1", "via1", "metal2"),
                                 offset   = in_v_line_offset)
                i += 1
        debug.info(1, "Done syndrome to locator bus route")

    def add_corrector(self):
        debug.info(1, "Starting to layout corrector logic")
        self.current_global_yoffset+=drc["minwidth_metal1"]/2
        for i in range(self.word_size):
            name = "corrector_pinv_{0}".format(i)
            #calculate position
            nand_2_label = "nand_2_a_{0}_0".format(i)
            a_position = self.locator_positions[nand_2_label]
            pinv_w = getattr(self.pinv, "width")
            pinv_position = vector(a_position[0]+pinv_w, self.current_global_yoffset)
            direction = "MY"
            #add current xor2 to the design
            self.add_inst(name = name, 
                          mod = self.pinv,
                          offset = pinv_position,
                          mirror = direction)
    
            #calculate input and output offsets
            pinv_input_position = getattr(self.pinv, "A_position")
            pinv_output_position = getattr(self.pinv, "Z_position")
            pinv_input_flip_x = (pinv_w-pinv_input_position[0])-pinv_w
            pinv_output_flip_x = (pinv_w-pinv_output_position[0])-pinv_w+drc["minwidth_metal3"]
            pinv_input_offset = pinv_position+\
                                vector(pinv_input_flip_x, pinv_input_position[1])
            pinv_output_offset = pinv_position+\
                                 vector(pinv_output_flip_x, pinv_output_position[1])


            #add labels/pins/connect
            self.add_label(text = "corrector_inv_a_{0}".format(i),
                           layer = "metal2",
                           offset = pinv_input_offset)
            self.add_label(text = "corrector_inv_z_{0}".format(i),
                           layer = "metal2",
                           offset = pinv_output_offset)
            self.add_pin("corrector_inv_a_{0}".format(i))
            self.add_pin("corrector_inv_z_{0}".format(i))
            self.connect_inst(["corrector_inv_a_{0}".format(i),
                               "corrector_inv_z_{0}".format(i),
                               "vdd",
                               "gnd"])
        
            minm1 = drc["minwidth_metal1"]
            inv_in_out_pair = [pinv_input_offset, pinv_output_offset]
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[0])
            self.add_via(layers   = ("metal1", "via1", "metal2"),
                         offset   = inv_in_out_pair[1])
            self.cor_label_positions["cor_inv_a_{0}".format(i)] = pinv_input_offset
            self.cor_label_positions["cor_inv_z_{0}".format(i)] = pinv_output_offset
            ################
            #place XOR gate
            ################
            name = "corrector_xor2_{0}".format(i)
            xor_2_position = vector(a_position[0], self.current_global_yoffset-drc["minwidth_metal1"]/2)
            a_flip_offset = vector(0,0)
            b_flip_offset = vector(0,0)
            out_flip_offset = vector(0,0)
            direction = "MX"
            xor_2_h = self.xor_2.height
            #a label
            a_y = xor_2_h-(xor_2_h-2*self.xor_2_chars["a"][1])
            a_flip_offset = vector(0,a_y)
            #b label
            b_y = xor_2_h-(xor_2_h-2*self.xor_2_chars["b"][1])
            b_flip_offset = vector(0, b_y)
            #out label
            out_y = xor_2_h-(xor_2_h-2*self.xor_2_chars["out"][1])
            out_flip_offset = vector(0, out_y)

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

            #add labels
            self.add_label(text = "corrector_a_{0}".format(i),
                           layer = "metal2",
                           offset = a_offset)
            self.add_label(text = "corrector_b_{0}".format(i),
                           layer = "metal2",
                           offset = b_offset)
            self.add_label(text = "corrector_out_{0}".format(i),
                           layer = "metal2",
                           offset = out_offset)

            #remember label positions for routing
            self.cor_label_positions["cor_xor2_a_{0}".format(i)] = a_offset
            self.cor_label_positions["cor_xor2_b_{0}".format(i)] = b_offset
            self.cor_label_positions["cor_xor2_out_{0}".format(i)] = out_offset

            #add pins
            self.add_pin("corrector_a_{0}".format(i))
            self.add_pin("corrector_b_{0}".format(i))
            self.add_pin("corrector_out_{0}".format(i))
            #connect
            self.connect_inst(["corrector_a_{0}".format(i),
                               "corrector_b_{0}".format(i),
                               "corrector_out_{0}".format(i),
                               "vdd",
                               "gnd"])
        #add gnd rail
        m1min = drc["minwidth_metal1"]
        w = self.parity_gen_width
        h = 2*m1min
        offset = vector(0, self.current_global_yoffset-m1min-m1min/2)
        self.add_rect(layer   = "metal1",
                      offset  = offset,
                      width   = w,
                      height  = h)
        self.add_label(text = "gnd",
                       layer = "metal1",
                       offset = offset+vector(m1min, m1min))
        #add vdd rail
        m1min = drc["minwidth_metal1"]
        w = self.parity_gen_width
        h = 2*m1min
        offset = vector(0, self.current_global_yoffset-m1min-m1min/2-self.xor_2.height)
        self.add_rect(layer   = "metal1",
                      offset  = offset,
                      width   = w,
                      height  = h)
        self.add_label(text = "vdd",
                       layer = "metal1",
                       offset = offset+vector(m1min, m1min))
            
        debug.info(1, "Done corrector logic layout")

    def route_corrector(self):
        debug.info(1, "Starting to route corrector logic")
        m2min = drc["minwidth_metal2"]
        m3min = drc["minwidth_metal3"]
        m2m = drc["metal2_to_metal2"]
        m3m = drc["metal3_to_metal3"]
        m3_extend_via2 = drc["metal3_extend_via2"] 
        print self.locator_output_gate
        
        #route locator output to the corrector input
        for i in range(self.word_size):
            #format label of the locator output gate
            label = "nand_2_z_{0}_{1}".format(i, self.locator_output_gate)
            #get source pin
            src = self.locator_positions[label]
            #format label of the corrector inverter gate
            label = "cor_inv_a_{0}".format(i)
            dest = self.cor_label_positions[label]
            #route 
            #vertical m2 from source up
            w = m2m
            h = src[1]-dest[1]
            offset = vector(src[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #horizontal m2 from src to destination
            w = src[0]-dest[0]
            h = m2min
            offset = vector(dest[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)

        #route corrector inverter to the corrector xor2
        for i in range(self.word_size):
            #format label of the corrector inverter output
            label = "cor_inv_z_{0}".format(i)
            #get source pin
            src = self.cor_label_positions[label]
            #format label of the corrector xor input b
            label = "cor_xor2_b_{0}".format(i)
            #get destination pin
            dest = self.cor_label_positions[label]
            ######
            #route
            ######
            #toggle yoffset to meet drc
            yoffset = src[1]-4*m3min+(i%2)*2*m3min
            #vertical m2 from source up to yoffset
            w = m2m
            h = src[1]-yoffset
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #vertical m2 from destination up to yoffset
            w = m2m
            h = yoffset-dest[1]
            offset = vector(dest[0], dest[1])
            self.add_rect(layer   = "metal2",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #horizontal m3 from src to destination on yoffset
            w = dest[0]-src[0]
            h = m3min
            offset = vector(src[0], yoffset)
            self.add_rect(layer   = "metal3",
                          offset  = offset,
                          width   = w,
                          height  = h)
            #add vias on both ends
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(src[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
            self.add_via(layers   = ("metal3", "via2", "metal2"),
                         offset   = vector(dest[0], yoffset)-vector(m3_extend_via2/2, m3_extend_via2/2))
            
        debug.info(1, "Done corrector logic route")
