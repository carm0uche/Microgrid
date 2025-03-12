from Data import *
from Classes import *

def calcul_power_PV(i):
    return PV_nb * Panneau_solaire.power * ppvCf[i]

def calcul_power_WT(i):
    return WT_nb * Eolienne.P_v[i]

def calcul_power_ENR(i):
    return calcul_power_PV(i) + calcul_power_WT(i)

def balance(i):
    return calcul_power_ENR >= load[i]

def set_energy_batt(v):
    if level_batt[-1] + v < 0:
        raise ValueError("Battery error : Energy level cannot be negative")
    level_batt.append(level_batt[-1] + v)

def set_energy_h2(v):
    if level_h2[-1] + v < 0:
        raise ValueError("H2 error : Energy level cannot be negative")
    level_h2.append(level_h2[-1] + v)   

def set_power_gen(v):
    Power_gen.append(v) 




    
    
