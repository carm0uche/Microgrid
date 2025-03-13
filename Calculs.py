from Data import *
from Classes import *

def calcul_power_PV(i):
    current_power = PV_nb * Panneau_solaire.power * ppvCf[i]
    Power_PV.append(current_power)
    return current_power

def calcul_power_WT(i):
    current_power = WT_nb * Eolienne.P_v[i]
    Power_WT.append(current_power)
    return current_power

def calcul_power_ENR(i):
    return calcul_power_PV(i) + calcul_power_WT(i)

def balance(i):
    return calcul_power_ENR >= load[i]

def set_energy_batt(v):
    if level_batt[-1] + v < 0.2*Batterie.capacity:
        print(f"Low battery at {date[i]}")
    if level_batt[-1] + v < 0:
        raise ValueError("Battery error : Energy level cannot be negative")
    level_batt.append(level_batt[-1] + v)

def set_energy_h2(v):
    if level_h2[-1] + v < 0:
        raise ValueError("H2 error : Energy level cannot be negative")
    level_h2.append(level_h2[-1] + v)   

def set_power_gen(v):
    Power_gen.append(v) 




    
    
