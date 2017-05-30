* OpenRAM generated memory.
* User: kabylkas
.global vdd gnd
*master-slave flip-flop with both output and inverted ouput

.subckt ms_flop din dout dout_bar clk vdd gnd
xmaster din mout mout_bar clk clk_bar vdd gnd dlatch
xslave mout_bar dout_bar dout clk_bar clk_nn vdd gnd dlatch
.ends flop

.subckt dlatch din dout dout_bar clk clk_bar vdd gnd
*clk inverter
mPff1 clk_bar clk vdd vdd p W=1.8u L=0.6u m=1
mNff1 clk_bar clk gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 1
mtmP1 din clk int1 vdd p W=1.8u L=0.6u m=1
mtmN1 din clk_bar int1 gnd n W=0.9u L=0.6u m=1

*foward inverter
mPff3 dout_bar int1 vdd vdd p W=1.8u L=0.6u m=1
mNff3 dout_bar int1 gnd gnd n W=0.9u L=0.6u m=1

*backward inverter
mPff4 dout dout_bar vdd vdd p W=1.8u L=0.6u m=1
mNf4 dout dout_bar gnd gnd n W=0.9u L=0.6u m=1

*transmission gate 2
mtmP2 int1 clk_bar dout vdd p W=1.8u L=0.6u m=1
mtmN2 int1 clk dout gnd n W=0.9u L=0.6u m=1
.ends dlatch


.SUBCKT nmos_m1_w1.2 D G S B
Mnmos D G S B n m=1 w=1.2u l=0.6u
.ENDS nmos_m1_w1.2

.SUBCKT pmos_m1_w2.4 D G S B
Mpmos D G S B p m=1 w=2.4u l=0.6u
.ENDS pmos_m1_w2.4

.SUBCKT pinv A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1.2
Xpinv_pmos Z A vdd vdd pmos_m1_w2.4
.ENDS pinv

.SUBCKT nmos_m1_w2.4 D G S B
Mnmos D G S B n m=1 w=2.4u l=0.6u
.ENDS nmos_m1_w2.4

.SUBCKT nand2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2.4
Xnmos2 net1 B gnd gnd nmos_m1_w2.4
Xpmos1 vdd A Z vdd pmos_m1_w2.4
Xpmos2 Z B vdd vdd pmos_m1_w2.4
.ENDS nand2

.SUBCKT nmos_m1_w3.6 D G S B
Mnmos D G S B n m=1 w=3.6u l=0.6u
.ENDS nmos_m1_w3.6

.SUBCKT NAND3 A B C Z vdd gnd
Xnmos1 net2 A gnd gnd nmos_m1_w3.6
Xnmos2 net1 B net2 gnd nmos_m1_w3.6
Xnmos3 Z C net1 gnd nmos_m1_w3.6
Xpmos1 Z A vdd vdd pmos_m1_w2.4
Xpmos2 vdd B Z vdd pmos_m1_w2.4
Xpmos3 Z C vdd vdd pmos_m1_w2.4
.ENDS NAND3

.SUBCKT nmos_m4_w1.2 D G S B
Mnmos D G S B n m=4 w=1.2u l=0.6u
.ENDS nmos_m4_w1.2

.SUBCKT pmos_m4_w2.4 D G S B
Mpmos D G S B p m=4 w=2.4u l=0.6u
.ENDS pmos_m4_w2.4

.SUBCKT pinv4 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m4_w1.2
Xpinv_pmos Z A vdd vdd pmos_m4_w2.4
.ENDS pinv4

.SUBCKT pmos_m4_w1.2 D G S B
Mpmos D G S B p m=4 w=1.2u l=0.6u
.ENDS pmos_m4_w1.2

.SUBCKT nor2 A B Z vdd gnd
Xnmos1 Z A gnd gnd nmos_m1_w1.2
Xnmos2 Z B gnd gnd nmos_m1_w1.2
Xpmos1 vdd A net1 vdd pmos_m4_w1.2
Xpmos2 net1 B Z vdd pmos_m4_w1.2
.ENDS nor2

.SUBCKT msf_control DATA[0] DATA[1] DATA[2] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] clk vdd gnd
XXdff0 DATA[0] data_in[0] data_in_bar[0] clk vdd gnd ms_flop
XXdff1 DATA[1] data_in[1] data_in_bar[1] clk vdd gnd ms_flop
XXdff2 DATA[2] data_in[2] data_in_bar[2] clk vdd gnd ms_flop
.ENDS msf_control

*********************** "cell_6t" ******************************
.SUBCKT replica_cell_6t bl br wl vdd gnd
M_1 gnd net_2 vdd vdd p W='0.9u' L=1.2u
M_2 net_2 gnd vdd vdd p W='0.9u' L=1.2u
M_3 br wl net_2 gnd n W='1.2u' L=0.6u
M_4 bl wl gnd gnd n W='1.2u' L=0.6u
M_5 net_2 gnd gnd gnd n W='2.4u' L=0.6u
M_6 gnd net_2 gnd gnd n W='2.4u' L=0.6u
.ENDS	$ replica_cell_6t

*********************** "cell_6t" ******************************
.SUBCKT cell_6t bl br wl vdd gnd
M_1 net_1 net_2 vdd vdd p W='0.9u' L=1.2u
M_2 net_2 net_1 vdd vdd p W='0.9u' L=1.2u
M_3 br wl net_2 gnd n W='1.2u' L=0.6u
M_4 bl wl net_1 gnd n W='1.2u' L=0.6u
M_5 net_2 net_1 gnd gnd n W='2.4u' L=0.6u
M_6 net_1 net_2 gnd gnd n W='2.4u' L=0.6u
.ENDS	$ cell_6t

.SUBCKT bitline_load bl[0] br[0] wl[0] wl[1] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
.ENDS bitline_load

.SUBCKT pmos_m1_w3.6 D G S B
Mpmos D G S B p m=1 w=3.6u l=0.6u
.ENDS pmos_m1_w3.6

.SUBCKT delay_chain_inv A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1.2
Xpinv_pmos Z A vdd vdd pmos_m1_w3.6
.ENDS delay_chain_inv

.SUBCKT delay_chain clk_in clk_out vdd gnd
Xinv_chain0 clk_in s1 vdd gnd delay_chain_inv
Xinv_chain1 s1 s2 vdd gnd delay_chain_inv
Xinv_chain2 s2 s3 vdd gnd delay_chain_inv
Xinv_chain3 s3 clk_out vdd gnd delay_chain_inv
.ENDS delay_chain

.SUBCKT RBL_inv A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1.2
Xpinv_pmos Z A vdd vdd pmos_m1_w3.6
.ENDS RBL_inv

.SUBCKT replica_bitline_nor2 A B Z vdd gnd
Xnmos1 Z A gnd gnd nmos_m1_w1.2
Xnmos2 Z B gnd gnd nmos_m1_w1.2
Xpmos1 vdd A net1 vdd pmos_m4_w1.2
Xpmos2 net1 B Z vdd pmos_m4_w1.2
.ENDS replica_bitline_nor2

.SUBCKT pmos_m1_w1.2 D G S B
Mpmos D G S B p m=1 w=1.2u l=0.6u
.ENDS pmos_m1_w1.2

.SUBCKT replica_bitline en out vdd gnd
XBL_inv bl[0] out vdd gnd RBL_inv
XBL_access_tx vdd delayed_en bl[0] vdd pmos_m1_w1.2
Xdelay_chain en delayed_en vdd gnd delay_chain
Xbitcell bl[0] br[0] delayed_en vdd gnd replica_cell_6t
Xload bl[0] br[0] gnd gnd vdd gnd bitline_load
.ENDS replica_bitline

.SUBCKT control_logic CSb WEb OEb s_en w_en tri_en tri_en_bar clk_bar clk vdd gnd
Xmsf_control CSb WEb OEb CS_bar CS WE_bar WE OE_bar OE clk vdd gnd msf_control
Xclk_inverter clk clk_bar vdd gnd pinv4
Xnor2 clk OE_bar tri_en vdd gnd nor2
Xnand2_tri_en OE clk_bar tri_en_bar vdd gnd nand2
Xreplica_bitline rblk pre_s_en vdd gnd replica_bitline
Xinv_s_en1 pre_s_en_bar s_en vdd gnd pinv
Xinv_s_en2 pre_s_en pre_s_en_bar vdd gnd pinv
XNAND3_rblk_bar clk_bar OE CS rblk_bar vdd gnd NAND3
XNAND3_w_en_bar clk_bar WE CS w_en_bar vdd gnd NAND3
Xinv_rblk rblk_bar rblk vdd gnd pinv
Xinv_w_en w_en_bar pre_w_en vdd gnd pinv
Xinv_w_en1 pre_w_en pre_w_en1 vdd gnd pinv
Xinv_w_en2 pre_w_en1 w_en vdd gnd pinv
.ENDS control_logic

.SUBCKT bitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd
Xbit_r0_c0 bl[0] br[0] wl[0] vdd gnd cell_6t
Xbit_r1_c0 bl[0] br[0] wl[1] vdd gnd cell_6t
Xbit_r2_c0 bl[0] br[0] wl[2] vdd gnd cell_6t
Xbit_r3_c0 bl[0] br[0] wl[3] vdd gnd cell_6t
Xbit_r4_c0 bl[0] br[0] wl[4] vdd gnd cell_6t
Xbit_r5_c0 bl[0] br[0] wl[5] vdd gnd cell_6t
Xbit_r6_c0 bl[0] br[0] wl[6] vdd gnd cell_6t
Xbit_r7_c0 bl[0] br[0] wl[7] vdd gnd cell_6t
Xbit_r8_c0 bl[0] br[0] wl[8] vdd gnd cell_6t
Xbit_r9_c0 bl[0] br[0] wl[9] vdd gnd cell_6t
Xbit_r10_c0 bl[0] br[0] wl[10] vdd gnd cell_6t
Xbit_r11_c0 bl[0] br[0] wl[11] vdd gnd cell_6t
Xbit_r12_c0 bl[0] br[0] wl[12] vdd gnd cell_6t
Xbit_r13_c0 bl[0] br[0] wl[13] vdd gnd cell_6t
Xbit_r14_c0 bl[0] br[0] wl[14] vdd gnd cell_6t
Xbit_r15_c0 bl[0] br[0] wl[15] vdd gnd cell_6t
Xbit_r0_c1 bl[1] br[1] wl[0] vdd gnd cell_6t
Xbit_r1_c1 bl[1] br[1] wl[1] vdd gnd cell_6t
Xbit_r2_c1 bl[1] br[1] wl[2] vdd gnd cell_6t
Xbit_r3_c1 bl[1] br[1] wl[3] vdd gnd cell_6t
Xbit_r4_c1 bl[1] br[1] wl[4] vdd gnd cell_6t
Xbit_r5_c1 bl[1] br[1] wl[5] vdd gnd cell_6t
Xbit_r6_c1 bl[1] br[1] wl[6] vdd gnd cell_6t
Xbit_r7_c1 bl[1] br[1] wl[7] vdd gnd cell_6t
Xbit_r8_c1 bl[1] br[1] wl[8] vdd gnd cell_6t
Xbit_r9_c1 bl[1] br[1] wl[9] vdd gnd cell_6t
Xbit_r10_c1 bl[1] br[1] wl[10] vdd gnd cell_6t
Xbit_r11_c1 bl[1] br[1] wl[11] vdd gnd cell_6t
Xbit_r12_c1 bl[1] br[1] wl[12] vdd gnd cell_6t
Xbit_r13_c1 bl[1] br[1] wl[13] vdd gnd cell_6t
Xbit_r14_c1 bl[1] br[1] wl[14] vdd gnd cell_6t
Xbit_r15_c1 bl[1] br[1] wl[15] vdd gnd cell_6t
Xbit_r0_c2 bl[2] br[2] wl[0] vdd gnd cell_6t
Xbit_r1_c2 bl[2] br[2] wl[1] vdd gnd cell_6t
Xbit_r2_c2 bl[2] br[2] wl[2] vdd gnd cell_6t
Xbit_r3_c2 bl[2] br[2] wl[3] vdd gnd cell_6t
Xbit_r4_c2 bl[2] br[2] wl[4] vdd gnd cell_6t
Xbit_r5_c2 bl[2] br[2] wl[5] vdd gnd cell_6t
Xbit_r6_c2 bl[2] br[2] wl[6] vdd gnd cell_6t
Xbit_r7_c2 bl[2] br[2] wl[7] vdd gnd cell_6t
Xbit_r8_c2 bl[2] br[2] wl[8] vdd gnd cell_6t
Xbit_r9_c2 bl[2] br[2] wl[9] vdd gnd cell_6t
Xbit_r10_c2 bl[2] br[2] wl[10] vdd gnd cell_6t
Xbit_r11_c2 bl[2] br[2] wl[11] vdd gnd cell_6t
Xbit_r12_c2 bl[2] br[2] wl[12] vdd gnd cell_6t
Xbit_r13_c2 bl[2] br[2] wl[13] vdd gnd cell_6t
Xbit_r14_c2 bl[2] br[2] wl[14] vdd gnd cell_6t
Xbit_r15_c2 bl[2] br[2] wl[15] vdd gnd cell_6t
.ENDS bitcell_array

.SUBCKT precharge_cell bl br clk vdd
Xlower_pmos bl clk br vdd pmos_m1_w1.2
Xupper_pmos1 bl clk vdd vdd pmos_m1_w2.4
Xupper_pmos2 br clk vdd vdd pmos_m1_w2.4
.ENDS precharge_cell

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] clk vdd
Xpre_column_0 bl[0] br[0] clk vdd precharge_cell
Xpre_column_1 bl[1] br[1] clk vdd precharge_cell
Xpre_column_2 bl[2] br[2] clk vdd precharge_cell
.ENDS precharge_array
*********************** "sense_amp" ******************************

.SUBCKT sense_amp bl br dout sclk vdd gnd
M_1 dout net_1 vdd vdd p W='5.4*1u' L=0.6u
M_2 dout net_1 net_2 gnd n W='2.7*1u' L=0.6u
M_3 net_1 dout vdd vdd p W='5.4*1u' L=0.6u
M_4 net_1 dout net_2 gnd n W='2.7*1u' L=0.6u
M_5 bl sclk dout vdd p W='7.2*1u' L=0.6u
M_6 br sclk net_1 vdd p W='7.2*1u' L=0.6u
M_7 net_2 sclk gnd gnd n W='2.7*1u' L=0.6u
.ENDS	 sense_amp


.SUBCKT sense_amp_array bl[0] br[0] bl[1] br[1] bl[2] br[2] data_out[0] data_out[1] data_out[2] sclk vdd gnd
Xsa_d0 bl[0] br[0] data_out[0] sclk vdd gnd sense_amp
Xsa_d1 bl[1] br[1] data_out[1] sclk vdd gnd sense_amp
Xsa_d2 bl[2] br[2] data_out[2] sclk vdd gnd sense_amp
.ENDS sense_amp_array
*********************** Write_Driver ******************************
.SUBCKT write_driver din bl br wen vdd gnd

**** Inverter to conver Data_in to data_in_bar ******
M_1 net_3 din gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 din vdd vdd p W='2.1*1u' L=0.6u

**** 2input nand gate follwed by inverter to drive BL ******
M_3 net_2 wen net_7 gnd n W='2.1*1u' L=0.6u
M_4 net_7 din gnd gnd n W='2.1*1u' L=0.6u
M_5 net_2 wen vdd vdd p W='2.1*1u' L=0.6u
M_6 net_2 din vdd vdd p W='2.1*1u' L=0.6u


M_7 net_1 net_2 vdd vdd p W='2.1*1u' L=0.6u
M_8 net_1 net_2 gnd gnd n W='1.2*1u' L=0.6u

**** 2input nand gate follwed by inverter to drive BR******

M_9 net_4 wen vdd vdd p W='2.1*1u' L=0.6u
M_10 net_4 wen net_8 gnd n W='2.1*1u' L=0.6u
M_11 net_8 net_3 gnd gnd n W='2.1*1u' L=0.6u
M_12 net_4 net_3 vdd vdd p W='2.1*1u' L=0.6u

M_13 net_6 net_4 vdd vdd p W='2.1*1u' L=0.6u
M_14 net_6 net_4 gnd gnd n W='1.2*1u' L=0.6u

************************************************

M_15 bl net_6 net_5 gnd n W='3.6*1u' L=0.6u
M_16 br net_1 net_5 gnd n W='3.6*1u' L=0.6u
M_17 net_5 wen gnd gnd n W='3.6*1u' L=0.6u



.ENDS	$ write_driver


.SUBCKT write_driver_array data_in[0] data_in[1] data_in[2] bl[0] br[0] bl[1] br[1] bl[2] br[2] wen vdd gnd
XXwrite_driver0 data_in[0] bl[0] br[0] wen vdd gnd write_driver
XXwrite_driver1 data_in[1] bl[1] br[1] wen vdd gnd write_driver
XXwrite_driver2 data_in[2] bl[2] br[2] wen vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinverter A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1.2
Xpinv_pmos Z A vdd vdd pmos_m1_w2.4
.ENDS pinverter

.SUBCKT pnand2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2.4
Xnmos2 net1 B gnd gnd nmos_m1_w2.4
Xpmos1 vdd A Z vdd pmos_m1_w2.4
Xpmos2 Z B vdd vdd pmos_m1_w2.4
.ENDS pnand2

.SUBCKT pnand3 A B C Z vdd gnd
Xnmos1 net2 A gnd gnd nmos_m1_w3.6
Xnmos2 net1 B net2 gnd nmos_m1_w3.6
Xnmos3 Z C net1 gnd nmos_m1_w3.6
Xpmos1 Z A vdd vdd pmos_m1_w2.4
Xpmos2 vdd B Z vdd pmos_m1_w2.4
Xpmos3 Z C vdd vdd pmos_m1_w2.4
.ENDS pnand3

.SUBCKT a_inv_1 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1.2
Xpinv_pmos Z A vdd vdd pmos_m1_w2.4
.ENDS a_inv_1

.SUBCKT a_nand_2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2.4
Xnmos2 net1 B gnd gnd nmos_m1_w2.4
Xpmos1 vdd A Z vdd pmos_m1_w2.4
Xpmos2 Z B vdd vdd pmos_m1_w2.4
.ENDS a_nand_2

.SUBCKT pre2x4 A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd
XXpre2x4_inv[0] A[0] B[0] vdd gnd a_inv_1
XXpre2x4_inv[1] A[1] B[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[0] Z[0] out[0] vdd gnd a_inv_1
XXpre2x4_nand_inv[1] Z[1] out[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[2] Z[2] out[2] vdd gnd a_inv_1
XXpre2x4_nand_inv[3] Z[3] out[3] vdd gnd a_inv_1
XXpre2x4_nand[0] A[0] A[1] Z[3] vdd gnd a_nand_2
XXpre2x4_nand[1] B[0] A[1] Z[2] vdd gnd a_nand_2
XXpre2x4_nand[2] A[0] B[1] Z[1] vdd gnd a_nand_2
XXpre2x4_nand[3] B[0] B[1] Z[0] vdd gnd a_nand_2
.ENDS pre2x4

.SUBCKT a_nand_3 A B C Z vdd gnd
Xnmos1 net2 A gnd gnd nmos_m1_w3.6
Xnmos2 net1 B net2 gnd nmos_m1_w3.6
Xnmos3 Z C net1 gnd nmos_m1_w3.6
Xpmos1 Z A vdd vdd pmos_m1_w2.4
Xpmos2 vdd B Z vdd pmos_m1_w2.4
Xpmos3 Z C vdd vdd pmos_m1_w2.4
.ENDS a_nand_3

.SUBCKT pre3x8 A[0] A[1] A[2] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] vdd gnd
XXpre2x4_nand_inv[0] Z[0] out[0] vdd gnd a_inv_1
XXpre2x4_nand_inv[1] Z[1] out[1] vdd gnd a_inv_1
XXpre2x4_nand_inv[2] Z[2] out[2] vdd gnd a_inv_1
XXpre2x4_nand_inv[3] Z[3] out[3] vdd gnd a_inv_1
XXpre2x4_nand_inv[4] Z[4] out[4] vdd gnd a_inv_1
XXpre2x4_nand_inv[5] Z[5] out[5] vdd gnd a_inv_1
XXpre2x4_nand_inv[6] Z[6] out[6] vdd gnd a_inv_1
XXpre2x4_nand_inv[7] Z[7] out[7] vdd gnd a_inv_1
XXpre3x8_nand[0] A[0] A[1] A[2] Z[7] vdd gnd a_nand_3
XXpre3x8_nand[1] A[0] A[1] B[2] Z[6] vdd gnd a_nand_3
XXpre3x8_nand[2] A[0] B[1] A[2] Z[5] vdd gnd a_nand_3
XXpre3x8_nand[3] A[0] B[1] B[2] Z[4] vdd gnd a_nand_3
XXpre3x8_nand[4] B[0] A[1] A[2] Z[3] vdd gnd a_nand_3
XXpre3x8_nand[5] B[0] A[1] B[2] Z[2] vdd gnd a_nand_3
XXpre3x8_nand[6] B[0] B[1] A[2] Z[1] vdd gnd a_nand_3
XXpre3x8_nand[7] B[0] B[1] B[2] Z[0] vdd gnd a_nand_3
.ENDS pre3x8

.SUBCKT hierarchical_decoder A[0] A[1] A[2] A[3] decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre[1] A[2] A[3] out[4] out[5] out[6] out[7] vdd gnd pre2x4
XNAND2_[0] out[0] out[4] Z[0] vdd gnd pnand2
XNAND2_[1] out[0] out[5] Z[1] vdd gnd pnand2
XNAND2_[2] out[0] out[6] Z[2] vdd gnd pnand2
XNAND2_[3] out[0] out[7] Z[3] vdd gnd pnand2
XNAND2_[4] out[1] out[4] Z[4] vdd gnd pnand2
XNAND2_[5] out[1] out[5] Z[5] vdd gnd pnand2
XNAND2_[6] out[1] out[6] Z[6] vdd gnd pnand2
XNAND2_[7] out[1] out[7] Z[7] vdd gnd pnand2
XNAND2_[8] out[2] out[4] Z[8] vdd gnd pnand2
XNAND2_[9] out[2] out[5] Z[9] vdd gnd pnand2
XNAND2_[10] out[2] out[6] Z[10] vdd gnd pnand2
XNAND2_[11] out[2] out[7] Z[11] vdd gnd pnand2
XNAND2_[12] out[3] out[4] Z[12] vdd gnd pnand2
XNAND2_[13] out[3] out[5] Z[13] vdd gnd pnand2
XNAND2_[14] out[3] out[6] Z[14] vdd gnd pnand2
XNAND2_[15] out[3] out[7] Z[15] vdd gnd pnand2
XINVERTER_[0] Z[0] decode_out[0] vdd gnd pinverter
XINVERTER_[1] Z[1] decode_out[1] vdd gnd pinverter
XINVERTER_[2] Z[2] decode_out[2] vdd gnd pinverter
XINVERTER_[3] Z[3] decode_out[3] vdd gnd pinverter
XINVERTER_[4] Z[4] decode_out[4] vdd gnd pinverter
XINVERTER_[5] Z[5] decode_out[5] vdd gnd pinverter
XINVERTER_[6] Z[6] decode_out[6] vdd gnd pinverter
XINVERTER_[7] Z[7] decode_out[7] vdd gnd pinverter
XINVERTER_[8] Z[8] decode_out[8] vdd gnd pinverter
XINVERTER_[9] Z[9] decode_out[9] vdd gnd pinverter
XINVERTER_[10] Z[10] decode_out[10] vdd gnd pinverter
XINVERTER_[11] Z[11] decode_out[11] vdd gnd pinverter
XINVERTER_[12] Z[12] decode_out[12] vdd gnd pinverter
XINVERTER_[13] Z[13] decode_out[13] vdd gnd pinverter
XINVERTER_[14] Z[14] decode_out[14] vdd gnd pinverter
XINVERTER_[15] Z[15] decode_out[15] vdd gnd pinverter
.ENDS hierarchical_decoder

.SUBCKT msf_address ADDR[0] ADDR[1] ADDR[2] ADDR[3] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] addr_clk vdd gnd
XXdff0 ADDR[0] A[0] A_bar[0] addr_clk vdd gnd ms_flop
XXdff1 ADDR[1] A[1] A_bar[1] addr_clk vdd gnd ms_flop
XXdff2 ADDR[2] A[2] A_bar[2] addr_clk vdd gnd ms_flop
XXdff3 ADDR[3] A[3] A_bar[3] addr_clk vdd gnd ms_flop
.ENDS msf_address

.SUBCKT msf_data_in DATA[0] DATA[1] DATA[2] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] clk vdd gnd
XXdff0 DATA[0] data_in[0] data_in_bar[0] clk vdd gnd ms_flop
XXdff1 DATA[1] data_in[1] data_in_bar[1] clk vdd gnd ms_flop
XXdff2 DATA[2] data_in[2] data_in_bar[2] clk vdd gnd ms_flop
.ENDS msf_data_in

.SUBCKT msf_data_out data_out[0] data_out[1] data_out[2] tri_in[0] tri_in_bar[0] tri_in[1] tri_in_bar[1] tri_in[2] tri_in_bar[2] sclk vdd gnd
XXdff0 data_out[0] tri_in[0] tri_in_bar[0] sclk vdd gnd ms_flop
XXdff1 data_out[1] tri_in[1] tri_in_bar[1] sclk vdd gnd ms_flop
XXdff2 data_out[2] tri_in[2] tri_in_bar[2] sclk vdd gnd ms_flop
.ENDS msf_data_out
*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

M_1 net_2 in_inv gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 in_inv vdd vdd p W='2.4*1u' L=0.6u
M_3 out en_bar net_3 vdd p W='2.4*1u' L=0.6u
M_4 out en net_2 gnd n W='1.2*1u' L=0.6u
M_5 in_inv in vdd vdd p W='2.4*1u' L=0.6u
M_6 in_inv in gnd gnd n W='1.2*1u' L=0.6u


.ENDS	

.SUBCKT tri_gate_array tri_in[0] tri_in[1] tri_in[2] DATA[0] DATA[1] DATA[2] en en_bar vdd gnd
XXtri_gate0 tri_in[0] DATA[0] en en_bar vdd gnd tri_gate
XXtri_gate1 tri_in[1] DATA[1] en en_bar vdd gnd tri_gate
XXtri_gate2 tri_in[2] DATA[2] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT wordline_driver decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk vdd gnd
XWordline_driver_inv_clk0 clk clk_bar[0] vdd gnd pinverter
XWordline_driver_nand0 decode_out[0] clk_bar[0] net[0] vdd gnd pnand2
XWordline_driver_inv0 net[0] wl[0] vdd gnd pinverter
XWordline_driver_inv_clk1 clk clk_bar[1] vdd gnd pinverter
XWordline_driver_nand1 decode_out[1] clk_bar[1] net[1] vdd gnd pnand2
XWordline_driver_inv1 net[1] wl[1] vdd gnd pinverter
XWordline_driver_inv_clk2 clk clk_bar[2] vdd gnd pinverter
XWordline_driver_nand2 decode_out[2] clk_bar[2] net[2] vdd gnd pnand2
XWordline_driver_inv2 net[2] wl[2] vdd gnd pinverter
XWordline_driver_inv_clk3 clk clk_bar[3] vdd gnd pinverter
XWordline_driver_nand3 decode_out[3] clk_bar[3] net[3] vdd gnd pnand2
XWordline_driver_inv3 net[3] wl[3] vdd gnd pinverter
XWordline_driver_inv_clk4 clk clk_bar[4] vdd gnd pinverter
XWordline_driver_nand4 decode_out[4] clk_bar[4] net[4] vdd gnd pnand2
XWordline_driver_inv4 net[4] wl[4] vdd gnd pinverter
XWordline_driver_inv_clk5 clk clk_bar[5] vdd gnd pinverter
XWordline_driver_nand5 decode_out[5] clk_bar[5] net[5] vdd gnd pnand2
XWordline_driver_inv5 net[5] wl[5] vdd gnd pinverter
XWordline_driver_inv_clk6 clk clk_bar[6] vdd gnd pinverter
XWordline_driver_nand6 decode_out[6] clk_bar[6] net[6] vdd gnd pnand2
XWordline_driver_inv6 net[6] wl[6] vdd gnd pinverter
XWordline_driver_inv_clk7 clk clk_bar[7] vdd gnd pinverter
XWordline_driver_nand7 decode_out[7] clk_bar[7] net[7] vdd gnd pnand2
XWordline_driver_inv7 net[7] wl[7] vdd gnd pinverter
XWordline_driver_inv_clk8 clk clk_bar[8] vdd gnd pinverter
XWordline_driver_nand8 decode_out[8] clk_bar[8] net[8] vdd gnd pnand2
XWordline_driver_inv8 net[8] wl[8] vdd gnd pinverter
XWordline_driver_inv_clk9 clk clk_bar[9] vdd gnd pinverter
XWordline_driver_nand9 decode_out[9] clk_bar[9] net[9] vdd gnd pnand2
XWordline_driver_inv9 net[9] wl[9] vdd gnd pinverter
XWordline_driver_inv_clk10 clk clk_bar[10] vdd gnd pinverter
XWordline_driver_nand10 decode_out[10] clk_bar[10] net[10] vdd gnd pnand2
XWordline_driver_inv10 net[10] wl[10] vdd gnd pinverter
XWordline_driver_inv_clk11 clk clk_bar[11] vdd gnd pinverter
XWordline_driver_nand11 decode_out[11] clk_bar[11] net[11] vdd gnd pnand2
XWordline_driver_inv11 net[11] wl[11] vdd gnd pinverter
XWordline_driver_inv_clk12 clk clk_bar[12] vdd gnd pinverter
XWordline_driver_nand12 decode_out[12] clk_bar[12] net[12] vdd gnd pnand2
XWordline_driver_inv12 net[12] wl[12] vdd gnd pinverter
XWordline_driver_inv_clk13 clk clk_bar[13] vdd gnd pinverter
XWordline_driver_nand13 decode_out[13] clk_bar[13] net[13] vdd gnd pnand2
XWordline_driver_inv13 net[13] wl[13] vdd gnd pinverter
XWordline_driver_inv_clk14 clk clk_bar[14] vdd gnd pinverter
XWordline_driver_nand14 decode_out[14] clk_bar[14] net[14] vdd gnd pnand2
XWordline_driver_inv14 net[14] wl[14] vdd gnd pinverter
XWordline_driver_inv_clk15 clk clk_bar[15] vdd gnd pinverter
XWordline_driver_nand15 decode_out[15] clk_bar[15] net[15] vdd gnd pnand2
XWordline_driver_inv15 net[15] wl[15] vdd gnd pinverter
.ENDS wordline_driver

.SUBCKT pinv4x A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m4_w1.2
Xpinv_pmos Z A vdd vdd pmos_m4_w2.4
.ENDS pinv4x

.SUBCKT pnand2_x1 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2.4
Xnmos2 net1 B gnd gnd nmos_m1_w2.4
Xpmos1 vdd A Z vdd pmos_m1_w2.4
Xpmos2 Z B vdd vdd pmos_m1_w2.4
.ENDS pnand2_x1

.SUBCKT pnor2_x1 A B Z vdd gnd
Xnmos1 Z A gnd gnd nmos_m1_w1.2
Xnmos2 Z B gnd gnd nmos_m1_w1.2
Xpmos1 vdd A net1 vdd pmos_m4_w1.2
Xpmos2 net1 B Z vdd pmos_m4_w1.2
.ENDS pnor2_x1

.SUBCKT test_bank1 DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] s_en w_en tri_en_bar tri_en clk_bar clk vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] clk_bar vdd precharge_array
Xsense_amp_array bl[0] br[0] bl[1] br[1] bl[2] br[2] data_out[0] data_out[1] data_out[2] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] data_in[2] bl[0] br[0] bl[1] br[1] bl[2] br[2] w_en vdd gnd write_driver_array
Xdata_in_flop_array DATA[0] DATA[1] DATA[2] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] clk_bar vdd gnd msf_data_in
Xtrigate_data_array data_out[0] data_out[1] data_out[2] DATA[0] DATA[1] DATA[2] tri_en tri_en_bar vdd gnd tri_gate_array
Xaddress_decoder A[0] A[1] A[2] A[3] decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] vdd gnd hierarchical_decoder
Xwordline_driver decode_out[0] decode_out[1] decode_out[2] decode_out[3] decode_out[4] decode_out[5] decode_out[6] decode_out[7] decode_out[8] decode_out[9] decode_out[10] decode_out[11] decode_out[12] decode_out[13] decode_out[14] decode_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk vdd gnd wordline_driver
Xaddress_flop_array ADDR[0] ADDR[1] ADDR[2] ADDR[3] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] clk vdd gnd msf_address
.ENDS test_bank1

.SUBCKT ecc DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] CSb WEb OEb clk vdd gnd
Xbank0 DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] s_en w_en tri_en_bar tri_en clk_bar clk vdd gnd test_bank1
Xcontrol CSb WEb OEb s_en w_en tri_en tri_en_bar clk_bar clk vdd gnd control_logic
.ENDS ecc
