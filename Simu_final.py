from Data import *
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
#                Simulateur
# =========================================


def simulation(paramètres, durée = len(load), données = True, graphique = False):
    '''
    paramètres = [ WT, PV, Fuel, Batt, H2 ]
    --
    Simulation complète
    --
    Renvoie : LCOE, Bilan Carbone, Data
    '''

    def dispatch(i, Batterie_level, H2_level) :
        '''
        Dispatch de la production, stockage à l'heure i
        --
        Renvoie : le profil [WT, PV, Diesel, Batt, H2, Curtailment, Shedding]
        '''
        Puissance_WT = paramètres[0] * Eolienne.P_v[i]
        Puissance_PV = paramètres[1] * Panneau_solaire.power * ppvCf[i]

        # profile = [WT, PV, Diesel, Batt, H2, Curtailment, Shedding]
        latest_profile = [Puissance_WT, Puissance_PV, 0, Batterie_level, H2_level, 0, 0]

        Diff = Puissance_WT + Puissance_PV - load[i]
        Balance = Diff >= 0

        if Balance :

            # Charge de la batterie
            chargement_batt = min(Diff, Batterie.charge_pw_max * paramètres[3])
            charge_batt = min(Batterie_level + Batterie.efficiency * chargement_batt, Batterie.capacity * paramètres[3])
            
            latest_profile[3] = charge_batt

            Diff = Diff + (Batterie_level - charge_batt) / Batterie.efficiency

            # Charge du stockage hydrogène
            chargement_H2 = min(Diff, Stockage_hydrogene.charge_pw_max * paramètres[4])
            charge_H2 = min(H2_level + Stockage_hydrogene.efficiency[0] * chargement_H2, Stockage_hydrogene.capacity * paramètres[4])

            latest_profile[4] = charge_H2

            Diff = Diff + (H2_level - charge_H2) / Stockage_hydrogene.efficiency[0]

            # Curtailment
            latest_profile[5] = Diff

            return latest_profile

        Diff = - Diff
        
        # Utilisation de la batterie    
        dechargement_batt = min(Diff, Batterie.charge_pw_max * paramètres[3])
        decharge_batt = max(Batterie_level - dechargement_batt / Batterie.efficiency, Batterie.state_charge_min * Batterie.capacity * paramètres[3])

        latest_profile[3] = decharge_batt
        print(i,decharge_batt)
        Diff = Diff + (decharge_batt - Batterie_level) * Batterie.efficiency
        
        # Utilisation de l'hydrogène
        dechargement_H2 = min(Diff, Stockage_hydrogene.charge_pw_max * paramètres[4])
        decharge_H2 = max(H2_level - dechargement_H2 / Stockage_hydrogene.efficiency[1], 0)

        latest_profile[4] = decharge_H2

        Diff = Diff + (decharge_H2 - H2_level) * Stockage_hydrogene.efficiency[1]

        #Utilisation du générateur
        puissance_gen = min(Diff, Generateur_diesel.max_power * paramètres[2])

        latest_profile[2] = puissance_gen

        Diff -= puissance_gen
        
        #Shedding
        latest_profile[6] = Diff

        return latest_profile

    batt_init_value = 0.5 * Batterie.capacity * paramètres[3]
    h2_init_value = 0.5 * Stockage_hydrogene.capacity * paramètres[4]
    
    profile = [[dispatch(0, batt_init_value, h2_init_value)[0]],
               [dispatch(0, batt_init_value, h2_init_value)[1]],
               [dispatch(0, batt_init_value, h2_init_value)[2]],
               [dispatch(0, batt_init_value, h2_init_value)[3]],
               [dispatch(0, batt_init_value, h2_init_value)[4]],
               [dispatch(0, batt_init_value, h2_init_value)[5]],
               [dispatch(0, batt_init_value, h2_init_value)[6]],]
            
    for i in range(1,durée):

        current_profile = dispatch(i, profile[3][-1], profile[4][-1])
        for j in range(7):
            profile[j].append(current_profile[j])

    # Calcul_LCOE
    LCOE = None

    # Bilan Carbone 
    BC = sum((0.05 * int(P/1000) + 1) + 0.236 * P for P in profile[2]) * 2.7 + 700000 * paramètres[0] + 50 * paramètres[1]

    if données :
        rendu = (LCOE, BC, profile)
    else :
        rendu = (LCOE,BC)
        
    if graphique :
        # Affichage graphique
    return rendu






















