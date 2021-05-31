from math import *
from prefixes import *
from resistor_rounder import round_map_vals

def calc_vo_from_vre(v_re_chosen:float):
    global v_re
    global v_o_max
    global power_to_load
    global v_cc
    global r_load
    v_re = v_re_chosen

    # Calc max and power from specified vre
    v_o_max = v_cc -(trans_vce_sat[5] + trans_vbe_veb_on[1] + trans_vbe_veb_on[2] + v_re_chosen) # Re chosen as 1 here
    # Power calc
    power_to_load = (v_o_max*v_o_max)/(2*r_load)

def calc_vo_from_power(power_to_load_chosen:float):
    global v_re
    global v_o_max
    global power_to_load
    global v_cc
    global r_load
    power_to_load = power_to_load_chosen

    v_o_max = sqrt(power_to_load*2*r_load) 

    # Calc max and power from specified vre
    v_re = v_cc - trans_vce_sat[5] - trans_vbe_veb_on[1] - trans_vbe_veb_on[2] - v_o_max

global_log_start_index = len(globals())+1

v_cc = 20
v_ee = -20
r_cable = 1*m
r_speaker = 8
r_load = r_cable+r_speaker

#Values that can be chosen START
I_CQ8 = 1*m
r_i_min_mult = 6.3
i_C6_min = 1.4*m
I_R1_i_C6_max_ratio = 0.5 # I_R1 = I_R1_i_C6_max_ratio * i_C6_max
I_R1_i_B6_max_ratio = 5 # I_R1 = I_R1_i_B6_max_ratio * i_B6_max
I_C5_i_C5_min_ratio = 1.1 # I_C5 = I_C5_i_C5_min_ratio * i_C5_min
#Values that can be chosen END

# Array of various vbe/veb on values, use transitor number as index, dummy zero value added for easy access
trans_vbe_veb_on = [0]+[0.7]*8# Manualy chosen
#trans_vbe_veb_on = [0]+[0.75]*8 # From provided spice
trans_vbe_veb_on[2] = 0.6
trans_vbe_veb_on[4] = 0.6

# Same as above but these provide beta values
#trans_beta = [0]+[100]*7 # Manualy chosen
#trans_beta = [0]+[250,120,250,120,220,250,220,250] # From provided spice
trans_beta = [0]+[255.9,156.7,255.9,137.6,231.7,255.9,231.7,255.9] # From provided spice

# Same as above but these provide minimum beta values
trans_beta_min = [0]+[100]*8
trans_beta_min[2] = 50
trans_beta_min[4] = 50
# Same as above but these saturation values
trans_vce_sat = [0]+[0.1]*8

# Power needed to be delivered to load
power_to_load = 0
v_o_max = 0
v_re = 0

calc_vo_from_power(40)
v_re = 3
#calc_vo_from_vre(2)

# Voltage between two darlington bare bases
v_bb = sum([v for v in trans_vbe_veb_on[1:5]])


i_E2_max = I_L_max = v_o_max/r_load
i_C4_max = I_L_max

i_B1_max = i_E2_max/(trans_beta[1]*trans_beta[2])

i_C6_max = i_C6_min + i_B1_max

i_B6_max = i_C6_max/trans_beta_min[6]

#I_R1 = I_R1_i_C6_max_ratio*i_C6_max
I_R1 = I_R1_i_B6_max_ratio*i_B6_max

i_C5_min = i_C6_max + I_R1

I_C5 = I_C5_i_C5_min_ratio * i_C5_min

#Determine R_E
r_E = v_re/I_C5

# Determine R3 and R4
r_B5 = 0.1*r_E*trans_beta_min[5]
I_B5 = I_C5/trans_beta_min[5]
v_th5 = v_cc  - v_re - trans_vbe_veb_on[5] - I_B5*r_B5
r_3 = (v_cc*r_B5)/v_th5
r_4 = (r_3*v_th5)/(v_cc-v_th5)

# Determine vbe multiplier things
r1_div_r2 = (v_bb/trans_vbe_veb_on[6])-1
r_2 = (v_bb/I_R1)/(1+r1_div_r2) #################################Reghardt#######################################
r_1 = r_2*r1_div_r2


# Determine r5 and r6
I_E7 = I_C5
I_B7 = I_E7/trans_beta_min[7]
r_eq = v_bb/I_C5 + r_E
r_th7 = 0.1*r_eq*trans_beta[6]
v_th7 = 0 - trans_vbe_veb_on[4] - trans_vbe_veb_on[3] - trans_vbe_veb_on[7] - I_B7*r_th7

r_5 = (r_th7*(v_cc-v_ee))/(v_th7-v_ee)
r_6 = 1/(1/r_th7 - 1/r_5)
#Preamp design
# Preamp Va
pre_amp_va = -v_o_max/0.5
r_i = (0.5/(1*m))*r_i_min_mult



I_EQ8 = I_CQ8*(trans_beta_min[8]/(trans_beta_min[8]+1))
I_BQ8 = I_CQ8/trans_beta_min[8]

#r_E8 = -(trans_beta_min[8]*r_C8)/pre_amp_va -(trans_beta_min[8]*26*m)/I_CQ8


# Iterate to get Re

diff = 0

best_diff = 2**64
best_re = 0

for r in range(0,1*M,10):
    RB = (0.1*trans_beta_min[8]*r)
    Rib = (trans_beta_min[8]*26*m)/I_CQ8 +r*(trans_beta_min[8]+1)

    new_r_i = RB*Rib/(RB+Rib)
    diff = abs(r_i - new_r_i)

    if(diff < best_diff):
        best_diff = diff
        best_re = r

r_E8 = best_re                                                                                          # Reghardt
r_C8 = (pre_amp_va*((trans_beta_min[8]*26*m)/I_CQ8 + r_E8*(trans_beta_min[8]+1)))/(-trans_beta_min[8])  # Reghardt

r_th8 = 0.1*trans_beta_min[8]*r_E8

v_th8 = v_ee+I_EQ8*r_E8 + trans_vbe_veb_on[8]+I_BQ8*r_th8

r_7 = (r_th8*(v_cc-v_ee))/(v_th8-v_ee)
r_8 = 1/(1/r_th8 - 1/r_7)


""" for key in list(globals())[global_log_start_index:]:
    val = globals()[key]
    val = str(val) if type(val) != float and type(val) != int else format_number(val)
    print(key + " = " + val)

 """
spice_map = {
    "R1":r_1,
    "R2":r_2,
    "R3":r_3,
    "R4":r_4,
    "R5":r_5,
    "R6":r_6,
    "R7":r_7,
    "R8":r_8,
    "RE":r_E,
    "RC8":r_C8,
    "RE8":r_E8
}

# round to real values
spice_map = round_map_vals(spice_map)

f = open("22723269.cir")
new_file_lines = []
for line in f.readlines():
    # Search for key
    found = False
    for key in spice_map.keys():
        splitted = line.split(" ")
        if splitted[0] == key:
            splitted[-1] = str(spice_map[key]) + "\n"
            new_file_lines.append(" ".join(splitted))
            found = True
            break

    if not found:
        new_file_lines.append(line)
f.close()
f = open("22723269.cir","w")
f.writelines(new_file_lines)
f.close()



print("\n".join(list(map(lambda item: "%s\t:%s" % (item[0],format_number(item[1])), spice_map.items()))))



""" RB = (0.1*trans_beta_min[8]*r_E)
Rib = (trans_beta_min[8]*26*m)/I_CQ8 +r_E

new_r_i = RB*Rib/(RB+Rib)

print("")
 """

import subprocess
import os
p = subprocess.Popen(["ngspice_con", "testbench_p3.cir", "-b"], cwd=os.getcwd(), stdout=subprocess.PIPE)
output = p.communicate()[0].decode("utf-8").split("\n") 
print("\n".join(output[-24:]))
prev_out = open("prev_output", "a")
prev_out.writelines(output[-24:])
prev_out.close()
#p.kill()
#print()