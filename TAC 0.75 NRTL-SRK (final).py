# 21/05/21

########################
# SCRIPT TAC EVALUATION
#######################

import math  # loading the library math to determine pi

#### PARAMETERS
pi = math.pi
ft_m = 3.28084  # m to ft conversion factor
Sm = 0.6096 # Tray height in m
Sft = 2  # Tray height in ft
M_and_S = 1431.7 # Marshall and Swift index
Fm_vessel_SS = 2.25 # material factor for SS vessel
Fp_vessel_LPC = 1 # pressure factor for vessel at 1 atm
Fp_vessel_HPC = 1.05 # pressure factor for vessel at 10 atm
Fr_tray = 0     # constructive factor for the tray
Fd_tray = 1     # trays distance factor, it's 1 for 2ft
Fm_tray_SS = 1.70   # material factor for SS tray
Fd_kettle = 1.35    # constructive factor for Kettle
Fd_condenser = 0.8  # constructive factor for condenser
Fp_heat_exchanger = 0 # pressure factor for heat exchanger from 1 to 10 atm
Fm_heat_exchanger_SS = 2.81 # material factor for SS heat exchanger
U_condenser = 1.1  # heat transfer coefficient for the condenser in kW/m^2K
U_kettle = 1.2  # heat transfer coefficient for the reboiler in kW/m^2K
U_reboiler_org = 1.0  # heat transfer coefficient for the reboiler with 2 organic vapors in kW/m^2K
T_steam_11atm = 457.804 # Saturated steam temperature at 11 atm
T_water_in = 293.15  # refrigerant water temperature in K (input)
T_water_out = 313.15  # refrigerant water temperature in K (output)
Cp_water = 4.186  # specific heat for water in kJ/kg*K
latent_heat_steam_11atm = 1997.36 # latent heat for 11 atm saturated steam in kJ/kg
t = 8000 # annual operating time in h
water_cost = 0.00031701  # water cost in $/kg
steam_cost_11atm = 0.016314  # saturated steam (11 atm) cost in $/kg
payback_period = 3  # payback period in years

#### VARIABLES
roL_LPC = 777   # LPC liquid density in kg/m3
roV_LPC = 1.66  # LPC vapor density in kg/m3
roL_HPC = 708   # HPC liquid density in kg/m3
roV_HPC = 16.5  # HPC vapor density in kg/m3
V_LPC = 1.69619 # LPC vapor flowrate in m3/s
V_HPC = 0.27760 # HPC vapor flowrate in m3/s
N_trays_LPC = 44    # LPC number of trays
N_trays_HPC = 42    # HPC number of trays
Q_condenser_LPC = 8019600  # condenser duty for LPC in KJ/h
Q_reboiler_LPC = 7623400   # reboiler duty for LPC in KJ/h
Q_reboiler_HPC = 8468000   # reboiler duty for HPC in KJ/h
T_dist_LPC = 332.941    # LPC distillate temperature in K
T_res_LPC = 344.127     # LPC residue temperature in K
T_dist_HPC = 409.324    # HPC distillate temperature in K
T_res_HPC = 434.438     # HPC residue temperature in K

#### EQUATIONS

# Capital cost LPC:
column_diameter_LPC = 4.5*(V_LPC**0.5)*((roV_LPC/(roL_LPC-roV_LPC))**0.25)
column_height_LPC = (Sm*(N_trays_LPC-2)+4.6)
column_diameter_LPC_ft = column_diameter_LPC*ft_m
column_height_LPC_ft = column_height_LPC*ft_m
Fc_vessel_LPC = Fm_vessel_SS*Fp_vessel_LPC
vessel_cost_LPC = (M_and_S/280)*101.9*column_diameter_LPC_ft**1.066*column_height_LPC_ft**0.82*(2.18+Fc_vessel_LPC)
Fc_tray = Fr_tray+Fd_tray+Fm_tray_SS
trays_cost_LPC = N_trays_LPC*(M_and_S/280)*4.7*column_diameter_LPC_ft**1.55*Sft*Fc_tray
Fc_kettle = (Fd_kettle+Fp_heat_exchanger)*Fm_heat_exchanger_SS
Fc_condenser = (Fd_condenser+Fp_heat_exchanger)*Fm_heat_exchanger_SS
DeltaT_kettle_LPC = T_dist_HPC - T_res_LPC
DeltaT_condenser_LPC = ((T_dist_LPC - T_water_in)-(T_dist_LPC-T_water_out))/math.log((T_dist_LPC-T_water_in)/(T_dist_LPC-T_water_out))  # math.log() replace ln
A_kettle_LPC = (Q_reboiler_LPC/3600)/(U_reboiler_org*DeltaT_kettle_LPC)
A_kettle_LPC_ft = A_kettle_LPC*(ft_m**2)
A_condenser_LPC = (Q_condenser_LPC/3600)/(U_condenser*DeltaT_condenser_LPC)
A_condenser_LPC_ft = A_condenser_LPC * (ft_m ** 2)
kettle_cost_LPC = (M_and_S/280)*101.3*(A_kettle_LPC_ft**0.65)*(2.29+Fc_kettle)
condenser_cost_LPC = (M_and_S / 280) * 101.3 * (A_condenser_LPC_ft** 0.65) * (2.29 + Fc_condenser)
capital_cost_LPC = vessel_cost_LPC + trays_cost_LPC + kettle_cost_LPC + condenser_cost_LPC

# Capital cost HPC:
column_diameter_HPC = 4.5*(V_HPC**0.5)*((roV_HPC/(roL_HPC-roV_HPC))**0.25)
column_height_HPC = (Sm * (N_trays_HPC - 2) + 4.6)
column_diameter_HPC_ft = column_diameter_HPC*ft_m
column_height_HPC_ft = column_height_HPC*ft_m
Fc_vessel_HPC = Fm_vessel_SS * Fp_vessel_HPC
vessel_cost_HPC = (M_and_S / 280) * 101.9 * column_diameter_HPC_ft ** 1.066 * column_height_HPC_ft ** 0.82 * (2.18 + Fc_vessel_HPC)
trays_cost_HPC = N_trays_HPC * (M_and_S / 280) * 4.7 * column_diameter_HPC_ft ** 1.55 * Sft * Fc_tray
DeltaT_kettle_HPC = T_steam_11atm - T_res_HPC
A_kettle_HPC = (Q_reboiler_HPC/3600) / (U_kettle * DeltaT_kettle_HPC)
A_kettle_HPC_ft = A_kettle_HPC * (ft_m ** 2)
kettle_cost_HPC = (M_and_S / 280) * 101.3 * (A_kettle_HPC_ft ** 0.65) * (2.29 + Fc_kettle)
capital_cost_HPC = vessel_cost_HPC + trays_cost_HPC + kettle_cost_HPC

# Annual operating cost LPC:
F_water_LPC = Q_condenser_LPC/(Cp_water*DeltaT_condenser_LPC)
water_cost_LPC = F_water_LPC*t*water_cost
annual_cost_LPC = water_cost_LPC

# Annual operating cost HPC:
V_steam_HPC = Q_reboiler_HPC/latent_heat_steam_11atm
steam_cost_HPC = V_steam_HPC*t*steam_cost_11atm
annual_cost_HPC = steam_cost_HPC

# TAC:
capital_cost = capital_cost_LPC + capital_cost_HPC
installation_cost = 0.60 * capital_cost
annual_operating_cost = annual_cost_LPC + annual_cost_HPC
TAC = ((capital_cost + installation_cost )/payback_period)+annual_operating_cost


#### PRINTING RESULTS

# Capital cost LPC:
print("column_diameter_LPC = " + str(column_diameter_LPC) + " m")  # str() to convert the numeric value to a string
print("column_height_LPC = " + str(column_height_LPC) + " m" )
print("vessel_cost_LPC = " + str(vessel_cost_LPC) + " $")
print("trays_cost_LPC = " + str(trays_cost_LPC) + " $")
print("DeltaT_kettle_LPC = " + str(DeltaT_kettle_LPC) + " K")
print("DeltaT_condenser_LPC = " + str(DeltaT_condenser_LPC) + " K")
print("A_kettle_LPC = " + str(A_kettle_LPC) + " m2")
print("A_condenser_LPC = " + str(A_condenser_LPC) + " m2")
print("kettle_cost_LPC = " + str(kettle_cost_LPC) + " $")
print("condenser_cost_LPC = " + str(condenser_cost_LPC) + " $")
print("capital_cost_LPC = " + str(capital_cost_LPC) + " $")
print("\n")  # to separate the results

# Capital cost HPC:
print("column_diameter_HPC = " + str(column_diameter_HPC) + " m")  # str() to convert the numeric value to a string
print("column_height_HPC = " + str(column_height_HPC) + " m")
print("vessel_cost_HPC = " + str(vessel_cost_HPC) + " $")
print("trays_cost_HPC = " + str(trays_cost_HPC) + " $")
print("DeltaT_kettle_HPC = " + str(DeltaT_kettle_HPC) + " K")
print("A_kettle_HPC = " + str(A_kettle_HPC) + " m2")
print("kettle_cost_HPC = " + str(kettle_cost_HPC) + " $")
print("capital_cost_HPC = " + str(capital_cost_HPC) + " $")
print("\n")

# Annual operating cost LPC:
print("F_water_LPC = " + str(F_water_LPC) + " Kg/h")
print("water_cost_LPC = " + str(water_cost_LPC) + " $/y")
print("annual_cost_LPC = " + str(annual_cost_LPC) + " $/y")
print("\n")

# Annual operating cost HPC:
print("V_steam_HPC = " + str(V_steam_HPC) + " Kg/h")
print("steam_cost_HPC = " + str(steam_cost_HPC) + " $/y")
print("annual_cost_HPC = " + str(annual_cost_HPC) + " $/y")
print("\n")

# TAC:
print("capital_cost = " + str(capital_cost) + " $")
print("installation_cost = " + str(installation_cost) + " $")
print("annual_operating_cost = " + str(annual_operating_cost) + " $/y")
print("TAC = " + str(TAC) + " $/y")

