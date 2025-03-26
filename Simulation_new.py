from Classes import *
from Calculs_new import *
from Data import *
from calcul_LCOE import *


def simulation_microgrid(params):

    #Simulation avec les paramètres correspondants
    Simu = calcul_simu(params)

    #Calcul shortage (on somme tous les shortages de la liste)
    Stg = - sum(Simu[6])

    #Calcul du bilan carbone global - 2.7kg de CO2 par litre de diesel brûlé
    BC = sum(50 + 0.236 * P for P in Simu[3]) * 2.7

    #Calcul de la LCOE avec la fonction de Baptiste
    LCOE = calcul_LCOE_simu(params, Simu)

    return LCOE, BC, Stg









