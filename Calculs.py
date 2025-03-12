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


    
    
