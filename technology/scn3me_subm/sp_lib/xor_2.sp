*********************** "xor_2" ******************************
.subckt xor_2 a b out vdd gnd
M1000 a_n11_24# a vdd Vdd pfet w=16 l=2
M1001 vdd a a_n2_58# Vdd pfet w=4 l=2
M1002 a_13_58# a_n11_24# vdd Vdd pfet w=4 l=2
M1003 out b a_13_58# Vdd pfet w=4 l=2
M1004 a_n2_58# a_29_22# out Vdd pfet w=4 l=2
M1005 a_n11_24# a gnd Gnd nfet w=8 l=2
M1006 vdd b a_29_22# Vdd pfet w=16 l=2
M1007 a_5_24# a gnd Gnd nfet w=4 l=2
M1008 out a_n11_24# a_5_24# Gnd nfet w=4 l=2
M1009 a_5_24# b out Gnd nfet w=4 l=2
M1010 gnd a_29_22# a_5_24# Gnd nfet w=4 l=2
M1011 gnd b a_29_22# Gnd nfet w=8 l=2
.ENDS xor_2
