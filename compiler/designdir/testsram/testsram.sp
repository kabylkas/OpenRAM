* OpenRAM generated memory.

.SUBCKT nmos_m1_w2_4 D G S B
Mnmos D G S B n m=1 w=2.4u l=0.6u
.ENDS nmos_m1_w2_4

.SUBCKT pmos_m1_w2_4 D G S B
Mpmos D G S B p m=1 w=2.4u l=0.6u
.ENDS pmos_m1_w2_4

.SUBCKT nand2_1 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2_4
Xnmos2 net1 B gnd gnd nmos_m1_w2_4
Xpmos1 vdd A Z vdd pmos_m1_w2_4
Xpmos2 Z B vdd vdd pmos_m1_w2_4
.ENDS nand2_1

.SUBCKT nmos_m1_w3_6_c1 D G S B
Mnmos D G S B n m=1 w=3.6u l=0.6u
.ENDS nmos_m1_w3_6_c1

.SUBCKT nand3_1 A B C Z vdd gnd
Xnmos net2 A gnd gnd nmos_m1_w3_6_c1
Xnmos2 net1 B net2 gnd nmos_m1_w3_6_c1
Xnmos3 Z C net1 gnd nmos_m1_w3_6_c1
Xpmos1 Z A vdd vdd pmos_m1_w2_4
Xpmos2 vdd B Z vdd pmos_m1_w2_4
Xpmos3 Z C vdd vdd pmos_m1_w2_4
.ENDS nand3_1

.SUBCKT nmos_m1_w1_2 D G S B
Mnmos D G S B n m=1 w=1.2u l=0.6u
.ENDS nmos_m1_w1_2

.SUBCKT pmos_m1_w3_6 D G S B
Mpmos D G S B p m=1 w=3.6u l=0.6u
.ENDS pmos_m1_w3_6

.SUBCKT nor2_1 A B Z vdd gnd
Xnmos1 Z A gnd gnd nmos_m1_w1_2
Xnmos2 Z B gnd gnd nmos_m1_w1_2
Xpmos1 vdd A net1 vdd pmos_m1_w3_6
Xpmos2 net1 B Z vdd pmos_m1_w3_6
.ENDS nor2_1

.SUBCKT nmos_m1_w1_2_a_p D G S B
Mnmos D G S B n m=1 w=1.2u l=0.6u
.ENDS nmos_m1_w1_2_a_p

.SUBCKT pmos_m1_w2_4_a_p D G S B
Mpmos D G S B p m=1 w=2.4u l=0.6u
.ENDS pmos_m1_w2_4_a_p

.SUBCKT pinv1 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv1

.SUBCKT nmos_m2_w1_2_a_p D G S B
Mnmos D G S B n m=2 w=1.2u l=0.6u
.ENDS nmos_m2_w1_2_a_p

.SUBCKT pmos_m2_w2_4_a_p D G S B
Mpmos D G S B p m=2 w=2.4u l=0.6u
.ENDS pmos_m2_w2_4_a_p

.SUBCKT pinv2 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m2_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m2_w2_4_a_p
.ENDS pinv2

.SUBCKT nmos_m4_w1_2_a_p D G S B
Mnmos D G S B n m=4 w=1.2u l=0.6u
.ENDS nmos_m4_w1_2_a_p

.SUBCKT pmos_m4_w2_4_a_p D G S B
Mpmos D G S B p m=4 w=2.4u l=0.6u
.ENDS pmos_m4_w2_4_a_p

.SUBCKT pinv3 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m4_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m4_w2_4_a_p
.ENDS pinv3

.SUBCKT nmos_m8_w1_2_a_p D G S B
Mnmos D G S B n m=8 w=1.2u l=0.6u
.ENDS nmos_m8_w1_2_a_p

.SUBCKT pmos_m8_w2_4_a_p D G S B
Mpmos D G S B p m=8 w=2.4u l=0.6u
.ENDS pmos_m8_w2_4_a_p

.SUBCKT pinv4 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m8_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m8_w2_4_a_p
.ENDS pinv4

.SUBCKT nmos_m16_w1_2_a_p D G S B
Mnmos D G S B n m=16 w=1.2u l=0.6u
.ENDS nmos_m16_w1_2_a_p

.SUBCKT pmos_m16_w2_4_a_p D G S B
Mpmos D G S B p m=16 w=2.4u l=0.6u
.ENDS pmos_m16_w2_4_a_p

.SUBCKT pinv5 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m16_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m16_w2_4_a_p
.ENDS pinv5
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


.SUBCKT msf_control din[0] din[1] din[2] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
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

.SUBCKT pinv6 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv6

.SUBCKT delay_chain in out vdd gnd
Xdinv0 in s1 vdd gnd pinv6
Xdinv1 s1 s2 vdd gnd pinv6
Xdinv2 s2 s3 vdd gnd pinv6
Xdinv3 s3 out vdd gnd pinv6
.ENDS delay_chain

.SUBCKT pinv7 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv7

.SUBCKT pmos_m1_w1_2 D G S B
Mpmos D G S B p m=1 w=1.2u l=0.6u
.ENDS pmos_m1_w1_2

.SUBCKT replica_bitline en out vdd gnd
Xrbl_inv bl[0] out vdd gnd pinv7
Xrbl_access_tx vdd delayed_en bl[0] vdd pmos_m1_w1_2
Xdelay_chain en delayed_en vdd gnd delay_chain
Xbitcell bl[0] br[0] delayed_en vdd gnd replica_cell_6t
Xload bl[0] br[0] gnd gnd vdd gnd bitline_load
.ENDS replica_bitline

.SUBCKT control_logic csb web oeb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd
Xmsf_control oeb csb web oe_bar oe cs_bar cs we_bar we clk_buf vdd gnd msf_control
Xinv_clk1_bar clk clk1_bar vdd gnd pinv2
Xinv_clk2 clk1_bar clk2 vdd gnd pinv3
Xinv_clk_bar clk2 clk_bar vdd gnd pinv4
Xinv_clk_buf clk_bar clk_buf vdd gnd pinv5
Xnand3_rblk_bar clk_bar oe cs rblk_bar vdd gnd nand3_1
Xinv_rblk rblk_bar rblk vdd gnd pinv1
Xnor2_tri_en clk_buf oe_bar tri_en vdd gnd nor2_1
Xnand2_tri_en oe clk_bar tri_en_bar vdd gnd nand2_1
Xinv_s_en pre_s_en_bar s_en vdd gnd pinv1
Xinv_pre_s_en_bar pre_s_en pre_s_en_bar vdd gnd pinv1
Xnand3_w_en_bar clk_bar we cs w_en_bar vdd gnd nand3_1
Xinv_pre_w_en w_en_bar pre_w_en vdd gnd pinv1
Xinv_pre_w_en_bar pre_w_en pre_w_en_bar vdd gnd pinv1
Xinv_w_en2 pre_w_en_bar w_en vdd gnd pinv1
Xreplica_bitline rblk pre_s_en vdd gnd replica_bitline
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
Xlower_pmos bl clk br vdd pmos_m1_w1_2
Xupper_pmos1 bl clk vdd vdd pmos_m1_w2_4
Xupper_pmos2 br clk vdd vdd pmos_m1_w2_4
.ENDS precharge_cell

.SUBCKT precharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] en vdd
Xpre_column_0 bl[0] br[0] en vdd precharge_cell
Xpre_column_1 bl[1] br[1] en vdd precharge_cell
Xpre_column_2 bl[2] br[2] en vdd precharge_cell
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


.SUBCKT sense_amp_array data[0] bl[0] br[0] data[1] bl[1] br[1] data[2] bl[2] br[2] en vdd gnd
Xsa_d0 bl[0] br[0] data[0] en vdd gnd sense_amp
Xsa_d1 bl[1] br[1] data[1] en vdd gnd sense_amp
Xsa_d2 bl[2] br[2] data[2] en vdd gnd sense_amp
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


.SUBCKT write_driver_array data[0] data[1] data[2] bl_out[0] br_out[0] bl_out[1] br_out[1] bl_out[2] br_out[2] en vdd gnd
XXwrite_driver0 data[0] bl_out[0] br_out[0] en vdd gnd write_driver
XXwrite_driver1 data[1] bl_out[1] br_out[1] en vdd gnd write_driver
XXwrite_driver2 data[2] bl_out[2] br_out[2] en vdd gnd write_driver
.ENDS write_driver_array

.SUBCKT pinv8 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv8

.SUBCKT nand2_2 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2_4
Xnmos2 net1 B gnd gnd nmos_m1_w2_4
Xpmos1 vdd A Z vdd pmos_m1_w2_4
Xpmos2 Z B vdd vdd pmos_m1_w2_4
.ENDS nand2_2

.SUBCKT nand3_2 A B C Z vdd gnd
Xnmos net2 A gnd gnd nmos_m1_w3_6_c1
Xnmos2 net1 B net2 gnd nmos_m1_w3_6_c1
Xnmos3 Z C net1 gnd nmos_m1_w3_6_c1
Xpmos1 Z A vdd vdd pmos_m1_w2_4
Xpmos2 vdd B Z vdd pmos_m1_w2_4
Xpmos3 Z C vdd vdd pmos_m1_w2_4
.ENDS nand3_2

.SUBCKT pinv9 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv9

.SUBCKT nand2_3 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2_4
Xnmos2 net1 B gnd gnd nmos_m1_w2_4
Xpmos1 vdd A Z vdd pmos_m1_w2_4
Xpmos2 Z B vdd vdd pmos_m1_w2_4
.ENDS nand2_3

.SUBCKT pre2x4 in[0] in[1] out[0] out[1] out[2] out[3] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv9
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv9
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv9
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv9
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv9
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv9
XXpre2x4_nand[0] in[0] in[1] Z[3] vdd gnd nand2_3
XXpre2x4_nand[1] inbar[0] in[1] Z[2] vdd gnd nand2_3
XXpre2x4_nand[2] in[0] inbar[1] Z[1] vdd gnd nand2_3
XXpre2x4_nand[3] inbar[0] inbar[1] Z[0] vdd gnd nand2_3
.ENDS pre2x4

.SUBCKT pinv10 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv10

.SUBCKT nand3_3 A B C Z vdd gnd
Xnmos net2 A gnd gnd nmos_m1_w3_6_c1
Xnmos2 net1 B net2 gnd nmos_m1_w3_6_c1
Xnmos3 Z C net1 gnd nmos_m1_w3_6_c1
Xpmos1 Z A vdd vdd pmos_m1_w2_4
Xpmos2 vdd B Z vdd pmos_m1_w2_4
Xpmos3 Z C vdd vdd pmos_m1_w2_4
.ENDS nand3_3

.SUBCKT pre3x8 in[0] in[1] in[2] out[0] out[1] out[2] out[3] out[4] out[5] out[6] out[7] vdd gnd
XXpre_inv[0] in[0] inbar[0] vdd gnd pinv10
XXpre_inv[1] in[1] inbar[1] vdd gnd pinv10
XXpre_inv[2] in[2] inbar[2] vdd gnd pinv10
XXpre_nand_inv[0] Z[0] out[0] vdd gnd pinv10
XXpre_nand_inv[1] Z[1] out[1] vdd gnd pinv10
XXpre_nand_inv[2] Z[2] out[2] vdd gnd pinv10
XXpre_nand_inv[3] Z[3] out[3] vdd gnd pinv10
XXpre_nand_inv[4] Z[4] out[4] vdd gnd pinv10
XXpre_nand_inv[5] Z[5] out[5] vdd gnd pinv10
XXpre_nand_inv[6] Z[6] out[6] vdd gnd pinv10
XXpre_nand_inv[7] Z[7] out[7] vdd gnd pinv10
XXpre3x8_nand[0] in[0] in[1] in[2] Z[7] vdd gnd nand3_3
XXpre3x8_nand[1] in[0] in[1] inbar[2] Z[6] vdd gnd nand3_3
XXpre3x8_nand[2] in[0] inbar[1] in[2] Z[5] vdd gnd nand3_3
XXpre3x8_nand[3] in[0] inbar[1] inbar[2] Z[4] vdd gnd nand3_3
XXpre3x8_nand[4] inbar[0] in[1] in[2] Z[3] vdd gnd nand3_3
XXpre3x8_nand[5] inbar[0] in[1] inbar[2] Z[2] vdd gnd nand3_3
XXpre3x8_nand[6] inbar[0] inbar[1] in[2] Z[1] vdd gnd nand3_3
XXpre3x8_nand[7] inbar[0] inbar[1] inbar[2] Z[0] vdd gnd nand3_3
.ENDS pre3x8

.SUBCKT hierarchical_decoder_16rows A[0] A[1] A[2] A[3] decode[0] decode[1] decode[2] decode[3] decode[4] decode[5] decode[6] decode[7] decode[8] decode[9] decode[10] decode[11] decode[12] decode[13] decode[14] decode[15] vdd gnd
Xpre[0] A[0] A[1] out[0] out[1] out[2] out[3] vdd gnd pre2x4
Xpre[1] A[2] A[3] out[4] out[5] out[6] out[7] vdd gnd pre2x4
XDEC_NAND[0] out[0] out[4] Z[0] vdd gnd nand2_2
XDEC_NAND[1] out[0] out[5] Z[1] vdd gnd nand2_2
XDEC_NAND[2] out[0] out[6] Z[2] vdd gnd nand2_2
XDEC_NAND[3] out[0] out[7] Z[3] vdd gnd nand2_2
XDEC_NAND[4] out[1] out[4] Z[4] vdd gnd nand2_2
XDEC_NAND[5] out[1] out[5] Z[5] vdd gnd nand2_2
XDEC_NAND[6] out[1] out[6] Z[6] vdd gnd nand2_2
XDEC_NAND[7] out[1] out[7] Z[7] vdd gnd nand2_2
XDEC_NAND[8] out[2] out[4] Z[8] vdd gnd nand2_2
XDEC_NAND[9] out[2] out[5] Z[9] vdd gnd nand2_2
XDEC_NAND[10] out[2] out[6] Z[10] vdd gnd nand2_2
XDEC_NAND[11] out[2] out[7] Z[11] vdd gnd nand2_2
XDEC_NAND[12] out[3] out[4] Z[12] vdd gnd nand2_2
XDEC_NAND[13] out[3] out[5] Z[13] vdd gnd nand2_2
XDEC_NAND[14] out[3] out[6] Z[14] vdd gnd nand2_2
XDEC_NAND[15] out[3] out[7] Z[15] vdd gnd nand2_2
XDEC_INV_[0] Z[0] decode[0] vdd gnd pinv8
XDEC_INV_[1] Z[1] decode[1] vdd gnd pinv8
XDEC_INV_[2] Z[2] decode[2] vdd gnd pinv8
XDEC_INV_[3] Z[3] decode[3] vdd gnd pinv8
XDEC_INV_[4] Z[4] decode[4] vdd gnd pinv8
XDEC_INV_[5] Z[5] decode[5] vdd gnd pinv8
XDEC_INV_[6] Z[6] decode[6] vdd gnd pinv8
XDEC_INV_[7] Z[7] decode[7] vdd gnd pinv8
XDEC_INV_[8] Z[8] decode[8] vdd gnd pinv8
XDEC_INV_[9] Z[9] decode[9] vdd gnd pinv8
XDEC_INV_[10] Z[10] decode[10] vdd gnd pinv8
XDEC_INV_[11] Z[11] decode[11] vdd gnd pinv8
XDEC_INV_[12] Z[12] decode[12] vdd gnd pinv8
XDEC_INV_[13] Z[13] decode[13] vdd gnd pinv8
XDEC_INV_[14] Z[14] decode[14] vdd gnd pinv8
XDEC_INV_[15] Z[15] decode[15] vdd gnd pinv8
.ENDS hierarchical_decoder_16rows

.SUBCKT msf_address din[0] din[1] din[2] din[3] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] dout[3] dout_bar[3] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
XXdff3 din[3] dout[3] dout_bar[3] clk vdd gnd ms_flop
.ENDS msf_address

.SUBCKT msf_data_in din[0] din[1] din[2] dout[0] dout_bar[0] dout[1] dout_bar[1] dout[2] dout_bar[2] clk vdd gnd
XXdff0 din[0] dout[0] dout_bar[0] clk vdd gnd ms_flop
XXdff1 din[1] dout[1] dout_bar[1] clk vdd gnd ms_flop
XXdff2 din[2] dout[2] dout_bar[2] clk vdd gnd ms_flop
.ENDS msf_data_in
*********************** tri_gate ******************************

.SUBCKT tri_gate in out en en_bar vdd gnd

M_1 net_2 in_inv gnd gnd n W='1.2*1u' L=0.6u
M_2 net_3 in_inv vdd vdd p W='2.4*1u' L=0.6u
M_3 out en_bar net_3 vdd p W='2.4*1u' L=0.6u
M_4 out en net_2 gnd n W='1.2*1u' L=0.6u
M_5 in_inv in vdd vdd p W='2.4*1u' L=0.6u
M_6 in_inv in gnd gnd n W='1.2*1u' L=0.6u


.ENDS	

.SUBCKT tri_gate_array in[0] in[1] in[2] out[0] out[1] out[2] en en_bar vdd gnd
XXtri_gate0 in[0] out[0] en en_bar vdd gnd tri_gate
XXtri_gate1 in[1] out[1] en en_bar vdd gnd tri_gate
XXtri_gate2 in[2] out[2] en en_bar vdd gnd tri_gate
.ENDS tri_gate_array

.SUBCKT pinv11 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv11

.SUBCKT nand2_4 A B Z vdd gnd
Xnmos1 Z A net1 gnd nmos_m1_w2_4
Xnmos2 net1 B gnd gnd nmos_m1_w2_4
Xpmos1 vdd A Z vdd pmos_m1_w2_4
Xpmos2 Z B vdd vdd pmos_m1_w2_4
.ENDS nand2_4

.SUBCKT wordline_driver in[0] in[1] in[2] in[3] in[4] in[5] in[6] in[7] in[8] in[9] in[10] in[11] in[12] in[13] in[14] in[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] en vdd gnd
Xwl_driver_inv_en0 en en_bar[0] vdd gnd pinv11
Xwl_driver_nand0 in[0] en_bar[0] net[0] vdd gnd nand2_4
Xwl_driver_inv0 net[0] wl[0] vdd gnd pinv11
Xwl_driver_inv_en1 en en_bar[1] vdd gnd pinv11
Xwl_driver_nand1 in[1] en_bar[1] net[1] vdd gnd nand2_4
Xwl_driver_inv1 net[1] wl[1] vdd gnd pinv11
Xwl_driver_inv_en2 en en_bar[2] vdd gnd pinv11
Xwl_driver_nand2 in[2] en_bar[2] net[2] vdd gnd nand2_4
Xwl_driver_inv2 net[2] wl[2] vdd gnd pinv11
Xwl_driver_inv_en3 en en_bar[3] vdd gnd pinv11
Xwl_driver_nand3 in[3] en_bar[3] net[3] vdd gnd nand2_4
Xwl_driver_inv3 net[3] wl[3] vdd gnd pinv11
Xwl_driver_inv_en4 en en_bar[4] vdd gnd pinv11
Xwl_driver_nand4 in[4] en_bar[4] net[4] vdd gnd nand2_4
Xwl_driver_inv4 net[4] wl[4] vdd gnd pinv11
Xwl_driver_inv_en5 en en_bar[5] vdd gnd pinv11
Xwl_driver_nand5 in[5] en_bar[5] net[5] vdd gnd nand2_4
Xwl_driver_inv5 net[5] wl[5] vdd gnd pinv11
Xwl_driver_inv_en6 en en_bar[6] vdd gnd pinv11
Xwl_driver_nand6 in[6] en_bar[6] net[6] vdd gnd nand2_4
Xwl_driver_inv6 net[6] wl[6] vdd gnd pinv11
Xwl_driver_inv_en7 en en_bar[7] vdd gnd pinv11
Xwl_driver_nand7 in[7] en_bar[7] net[7] vdd gnd nand2_4
Xwl_driver_inv7 net[7] wl[7] vdd gnd pinv11
Xwl_driver_inv_en8 en en_bar[8] vdd gnd pinv11
Xwl_driver_nand8 in[8] en_bar[8] net[8] vdd gnd nand2_4
Xwl_driver_inv8 net[8] wl[8] vdd gnd pinv11
Xwl_driver_inv_en9 en en_bar[9] vdd gnd pinv11
Xwl_driver_nand9 in[9] en_bar[9] net[9] vdd gnd nand2_4
Xwl_driver_inv9 net[9] wl[9] vdd gnd pinv11
Xwl_driver_inv_en10 en en_bar[10] vdd gnd pinv11
Xwl_driver_nand10 in[10] en_bar[10] net[10] vdd gnd nand2_4
Xwl_driver_inv10 net[10] wl[10] vdd gnd pinv11
Xwl_driver_inv_en11 en en_bar[11] vdd gnd pinv11
Xwl_driver_nand11 in[11] en_bar[11] net[11] vdd gnd nand2_4
Xwl_driver_inv11 net[11] wl[11] vdd gnd pinv11
Xwl_driver_inv_en12 en en_bar[12] vdd gnd pinv11
Xwl_driver_nand12 in[12] en_bar[12] net[12] vdd gnd nand2_4
Xwl_driver_inv12 net[12] wl[12] vdd gnd pinv11
Xwl_driver_inv_en13 en en_bar[13] vdd gnd pinv11
Xwl_driver_nand13 in[13] en_bar[13] net[13] vdd gnd nand2_4
Xwl_driver_inv13 net[13] wl[13] vdd gnd pinv11
Xwl_driver_inv_en14 en en_bar[14] vdd gnd pinv11
Xwl_driver_nand14 in[14] en_bar[14] net[14] vdd gnd nand2_4
Xwl_driver_inv14 net[14] wl[14] vdd gnd pinv11
Xwl_driver_inv_en15 en en_bar[15] vdd gnd pinv11
Xwl_driver_nand15 in[15] en_bar[15] net[15] vdd gnd nand2_4
Xwl_driver_inv15 net[15] wl[15] vdd gnd pinv11
.ENDS wordline_driver

.SUBCKT pinv12 A Z vdd gnd
Xpinv_nmos Z A gnd gnd nmos_m1_w1_2_a_p
Xpinv_pmos Z A vdd vdd pmos_m1_w2_4_a_p
.ENDS pinv12

.SUBCKT bank DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd
Xbitcell_array bl[0] br[0] bl[1] br[1] bl[2] br[2] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] vdd gnd bitcell_array
Xprecharge_array bl[0] br[0] bl[1] br[1] bl[2] br[2] clk_bar vdd precharge_array
Xsense_amp_array data_out[0] bl[0] br[0] data_out[1] bl[1] br[1] data_out[2] bl[2] br[2] s_en vdd gnd sense_amp_array
Xwrite_driver_array data_in[0] data_in[1] data_in[2] bl[0] br[0] bl[1] br[1] bl[2] br[2] w_en vdd gnd write_driver_array
Xdata_in_flop_array DATA[0] DATA[1] DATA[2] data_in[0] data_in_bar[0] data_in[1] data_in_bar[1] data_in[2] data_in_bar[2] clk_bar vdd gnd msf_data_in
Xtri_gate_array data_out[0] data_out[1] data_out[2] DATA[0] DATA[1] DATA[2] tri_en tri_en_bar vdd gnd tri_gate_array
Xrow_decoder A[0] A[1] A[2] A[3] dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] vdd gnd hierarchical_decoder_16rows
Xwordline_driver dec_out[0] dec_out[1] dec_out[2] dec_out[3] dec_out[4] dec_out[5] dec_out[6] dec_out[7] dec_out[8] dec_out[9] dec_out[10] dec_out[11] dec_out[12] dec_out[13] dec_out[14] dec_out[15] wl[0] wl[1] wl[2] wl[3] wl[4] wl[5] wl[6] wl[7] wl[8] wl[9] wl[10] wl[11] wl[12] wl[13] wl[14] wl[15] clk_buf vdd gnd wordline_driver
Xaddress_flop_array ADDR[0] ADDR[1] ADDR[2] ADDR[3] A[0] A_bar[0] A[1] A_bar[1] A[2] A_bar[2] A[3] A_bar[3] clk_buf vdd gnd msf_address
.ENDS bank

.SUBCKT testsram DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] CSb WEb OEb clk vdd gnd
Xbank0 DATA[0] DATA[1] DATA[2] ADDR[0] ADDR[1] ADDR[2] ADDR[3] s_en w_en tri_en_bar tri_en clk_bar clk_buf vdd gnd bank
Xcontrol CSb WEb OEb clk s_en w_en tri_en tri_en_bar clk_bar clk_buf vdd gnd control_logic
.ENDS testsram
