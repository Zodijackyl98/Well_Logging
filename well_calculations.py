conversions = {'liter - gallon': 0.2641720524,
               'gallon - bbl': 0.0238095238,
               'meter - ft': 3.2808399,
               'ppcf - ppg': 0.13368055787372,
               'liter - bbl': 0.0062898108,
               'psi - bar': 0.0689475729
               }


bit_pos = 2792 * conversions['meter - ft'] #ft 
TD = 2792 * conversions['meter - ft'] #in ft
TVD = 2707.69 * conversions['meter - ft'] #in ft
length_DC = 139.65 * conversions['meter - ft'] #in ft
length_HWDP = 112.44 * conversions['meter - ft'] #in ft
length_DP = bit_pos - length_DC - length_HWDP

id_DC = 2.250 #inc
od_DC = 6.5 #inc
id_DP = 4.276 #inc
od_DP = 5 #inc
id_HWDP = 3 #inc
od_HWDP = 5 #inc
od_BIT = 8.5 #inc

mw = 64 * conversions['ppcf - ppg'] # mud weight ppcf to ppg
pv = 18 #cp plastic viscosity
Q = 503 #flowrate in in gpm
vf = (pv/mw)**0.14 #viscosity correction factor
c_dp = ((6.1)/((id_DP)**4.86)) # general coefficient factor for internal diameter of pipe
c_hwdp = ((6.1)/((id_HWDP)**4.86)) 
c_dc = ((6.1)/((id_DC)**4.86))


delta_psi_dp = 0.00001 * length_DP * c_dp * mw * vf * (Q**1.89)# pressure loss in dp # Default Q**1.86
delta_psi_hwdp = 0.00001 * length_HWDP * c_hwdp * mw * vf * (Q**1.89)# pressure loss in hwdp
delta_psi_dc = 0.00001 * length_DC* c_dc * mw * vf * (Q**1.89)# pressure loss in dc
total_loss_drill_string = delta_psi_dp + delta_psi_hwdp + delta_psi_dc #psi

b = 2.4 # between 2.0 and 2.5
id_casing = 8.681 # inch
casing_shoe = 2667 #meters
length_liner = 0
annular_V_dp = (24.5 * Q) / ((id_casing**2) - (od_DP**2))
annular_V_hwdp = (24.5 * Q) / ((id_casing**2) - (od_HWDP**2))
annular_V_dc = (24.5 * Q) / ((id_casing**2) - (od_DC**2))

c_dp_annular = (8.6 * b) / ((id_casing - id_DP) * ((id_casing**2) - (id_DP**2))**2)
delta_psi_annular_dp = 0.00001 * length_DP * c_dp_annular * mw * vf * (Q**1.86)

p_annular_dp = ((1.4327*10**-7) * mw * length_DP * annular_V_dp**1.86) / (id_casing - od_DP)
p_annular_hwdp = ((1.4327*10**-7) * mw * length_HWDP * annular_V_hwdp**1.86) / (id_casing - od_HWDP)
p_annular_dc = ((1.4327*10**-7) * mw * length_DC * annular_V_dc**1.86) / (id_casing - od_DC)
total_loss_annular = p_annular_dp + p_annular_hwdp + p_annular_dc #psi

tfa = ((3* (20**2))) / 1308.8 #square inch
total_loss_bit = ((Q**2) * mw) / (12031 * tfa**2) #psi

total_loss_DHM = 375 #Down Hole Motor 375psi at 500gpm

se_c = 0.36# oefficient (1.0, 0.36, 0.22, 0.15)
se_loss = se_c * mw * (Q/100)**1.86 #psi

bhp_static = mw * TVD * 0.052 #psi
ecd = (mw + (((total_loss_annular)/(TVD*0.052)))) / (conversions['ppcf - ppg'])
bhp_dynamic = bhp_static + total_loss_annular


pump_output = 6.47010 #gal/stroke
efficiency = 0.97 
real_pump_output = pump_output * efficiency
spm_1 = 80 #stroke per min
spm_2 = 0 #stroke per min
spm_total = spm_1 + spm_2
flow_rate = real_pump_output * (spm_total) #gal/min

internal_vol_capacity_dp = ((id_DP**2) / 1029.4) * 3.281 * length_DP/conversions['meter - ft'] 
internal_vol_capacity_hwdp = ((id_HWDP**2) / 1029.4) * 3.281 * length_HWDP/conversions['meter - ft']
internal_vol_capacity_dc = ((id_DC**2) / 1029.4) * 3.281 * length_DC/conversions['meter - ft']
total_cap_ds = internal_vol_capacity_dp+internal_vol_capacity_dc+internal_vol_capacity_hwdp

internal_vol_capacity_liner = ((id_casing**2) / 1029.4) * 3.281 * length_liner # casing's ID is used
internal_vol_capacity_csg = ((id_casing**2) / 1029.4) * 3.281 * casing_shoe
internal_vol_capacity_oh = ((od_BIT**2) / 1029.4) * 3.281 * ((TD/ conversions['meter - ft']) - casing_shoe)
# internal_vol_capacity_annular = ((id_casing**2) / 1029.4) * bit_pos
total_cap_well = internal_vol_capacity_csg+internal_vol_capacity_oh+internal_vol_capacity_liner

displacement_dp = ((od_DP**2) / 1029.4) * 3.281 * length_DP /conversions['meter - ft'] 
displacement_hwdp = ((od_HWDP**2) / 1029.4) * 3.281 * length_HWDP /conversions['meter - ft']
displacement_dc = ((od_DC**2) / 1029.4) * 3.281 * length_DC /conversions['meter - ft']
total_displacement_ds = displacement_dc+displacement_dp+displacement_hwdp

annular_volume = total_cap_well - total_displacement_ds
steel_volume = total_displacement_ds - total_cap_ds

lag_time = (total_cap_well - total_displacement_ds) / (flow_rate * conversions['gallon - bbl'])
lag_strokes = (annular_volume) / (real_pump_output * conversions['gallon - bbl'])
down_time = (total_cap_ds) / (flow_rate * conversions['gallon - bbl'])
down_strokes = (total_cap_ds) / (real_pump_output * conversions['gallon - bbl'])
cycle_time = lag_time + down_time
cycle_strokes = lag_strokes + down_strokes

dp_weight = 19.5 #lb/ft
bha_weight = 60 #klb
td_weight = 51.7 #klb
string_weight_air = ((dp_weight* length_DP)/1000) + bha_weight #klb
steel_density = 65.5 #ppg
buoyoncy_factor = (steel_density - mw) / (steel_density)
string_weight_mud = string_weight_air * buoyoncy_factor
string_weight_total = string_weight_mud + td_weight

print("String Weight in Air = ", string_weight_air,'\n',
      "String Weight in Mud = ", string_weight_mud,'\n',
      "Total String Weight = ", string_weight_total, sep = '')

print("Bottom Hole Pressure(static) = {:<10}\nBottom Hole Pressure(dynamic) = {:<10}\nECD = {:<5}".format(bhp_static, bhp_dynamic, ecd))

print("Total Capacity of the Well = ", total_cap_well, "\n"
      "Total Capacity of Drill String = ", total_cap_ds, "\n"
      "Total Displacement of Drill String = ", total_displacement_ds, "\n"
      "Annular Volume = ", annular_volume, "\n"
      "Steel Volume = ", steel_volume)

print("Flow Rate(gpm) = ", flow_rate, "\n" 
      "Lag Time(min) = ", lag_time, "\n"
      "Lag Time(strokes) = ", lag_strokes, "\n"
      "Down Time(min) = ", down_time, "\n"
      "Down Time(strokes) = ", down_strokes, "\n"
      "Cycle Time(min) = ", cycle_time, "\n"
      "Cycle Time(strokes)", cycle_strokes, end = '\n'
)

print("Pressure Losses Through Drill String = {a:<6}\n \
      Total loss Through Annular = {b:<6}\n \
      Total loss of Bit = {c:<6}\n \
      Total Loss DHM = {d:<6}\n \
      Total Surface Loss = {e:<6}\n \
      Final Total pressure Loss = {f:<6}".format(
      a = total_loss_drill_string,
      b = total_loss_annular,
      c = total_loss_bit,
      d = total_loss_DHM,
      e = se_loss,
      f = total_loss_drill_string+total_loss_annular+total_loss_bit+ total_loss_DHM + se_loss))

variable_dict = {}
variables = [i for i in dir() if (i.startswith('_') == False) & ('plt' not in i) & ('np' not in i) & ('pd' not in i)& ('exit' not in i)& ('os' not in i)& ('quit' not in i) & ('variables' not in i)]

for i in variables[2:]:
      variable_dict[i] = vars()[i]

del variable_dict['variable_dict']

f = open('./drilling_variables_.txt', 'w+')

for i in variable_dict.keys():
      f.write(i + '\t' + str(variable_dict[i]) + '\n')

f.close()


# print(variable_dict)

