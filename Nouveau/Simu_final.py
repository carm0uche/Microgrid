from Data import *
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================
#                Simulateur
# =========================================


def simulation(paramètres, durée = 8760, données = True, graphique = False):
    '''
    paramètres = [ WT, PV, Fuel, Batt, H2 ]
    --
    Simulation complète
    --
    Renvoie : LCOE, Consommation de fuel, Profile
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
            charge_batt = min(Batterie_level + sqrt(Batterie.efficiency) * Diff, Batterie.capacity * paramètres[3])
            
            latest_profile[3] = charge_batt

            Diff = Diff + (Batterie_level - charge_batt) / sqrt(Batterie.efficiency)

            # Charge du stockage hydrogène
            chargement_H2 = min(Diff, paramètres[4][1])
            charge_H2 = min(H2_level + Stockage_hydrogene.efficiency[0] * chargement_H2, Stockage_hydrogene.capacity * paramètres[4][0])

            latest_profile[4] = charge_H2

            Diff = Diff + (H2_level - charge_H2) / Stockage_hydrogene.efficiency[0]

            # Curtailment
            latest_profile[5] = Diff
            
            return latest_profile

        Diff = - Diff
        
        # Utilisation de la batterie    
        decharge_batt = max(Batterie_level - Diff / sqrt(Batterie.efficiency), Batterie.state_charge_min * Batterie.capacity * paramètres[3])

        latest_profile[3] = decharge_batt
        Diff = Diff + (decharge_batt - Batterie_level) * sqrt(Batterie.efficiency)
        
        # Utilisation de l'hydrogène
        dechargement_H2 = min(Diff, paramètres[4][2])
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
    h2_init_value = 0.1 * Stockage_hydrogene.capacity * paramètres[4][0]
    
    profile0 = dispatch(0, batt_init_value, h2_init_value)

    profile = [[profile0[0]],
               [profile0[1]],
               [profile0[2]],
               [profile0[3]],
               [profile0[4]],
               [profile0[5]],
               [profile0[6]]]
            
    for i in range(1,durée):
        current_profile = dispatch(i, profile[3][-1], profile[4][-1])
        for j in range(7):
            profile[j].append(current_profile[j])

    # Consommation fuel 
    CF = sum((0.05 * int(P/1000) + 1) + 0.236 * P for P in profile[2]) * Lifetime

    # Calcul LCOE
    ## LCOE PV ------------------------
    Capex_PV = paramètres[1] * Panneau_solaire.capex * Panneau_solaire.power 
    Opex_PV = []
    opex_annuel_PV = Panneau_solaire.power * Panneau_solaire.opex * paramètres[1]
    for i in range(Lifetime) : 
        opex_annualise_PV = opex_annuel_PV/(1 + Discount_rate)**i
        Opex_PV.append(opex_annualise_PV)
    print("PV")
    
    ## WT ------------------------
    Capex_WT = Eolienne.capex * Eolienne.rated_power * paramètres[0]
    Opex_WT = []
    opex_annuel_WT = Eolienne.rated_power * Eolienne.opex * paramètres[0]
    for i in range(Lifetime) : 
        opex_annualise_WT = opex_annuel_WT/(1+Discount_rate)**i
        Opex_WT.append(opex_annualise_WT)

    ## Diesel ------------------------

    Capex_Diesel = paramètres[2] * Generateur_diesel.capex * Generateur_diesel.max_power * 1.26656907
    Opex_Diesel = []
    opex_annuel_Diesel = Generateur_diesel.max_power * Generateur_diesel.opex * paramètres[2]
    for i in range(Lifetime) : 
        opex_annualise_Diesel = opex_annuel_Diesel/(1+Discount_rate)**i
        Opex_Diesel.append(opex_annualise_Diesel)

    ## H2 -------  ------------------------- 

    Capex_H2 = (Stockage_hydrogene.capacity * Stockage_hydrogene.capex_tank / 33.3 * paramètres[4][0] + paramètres[4][1] * Stockage_hydrogene.capex_el +  paramètres[4][2] * Stockage_hydrogene.capex_fc) * 1.105034779
    Opex_H2 = []
    opex_annuel_H2 = Stockage_hydrogene.capacity * Stockage_hydrogene.opex_tank / 33.3 * paramètres[4][0] + paramètres[4][1] * Stockage_hydrogene.opex_el +  paramètres[4][2] * Stockage_hydrogene.opex_fc
    for i in range(Lifetime) : 
        opex_annualise_H2 = opex_annuel_H2/(1+Discount_rate)**i
        Opex_H2.append(opex_annualise_H2)

    ## Batt ------------------------------

    Capex_Batt = paramètres[3] * Batterie.capex * Batterie.capacity * 1.26656907
    Opex_Batt = []
    opex_annuel_Batt = Batterie.capacity * Batterie.opex * paramètres[3]
    for i in range(Lifetime) : 
        opex_annualise_Batt = opex_annuel_Batt/(1+Discount_rate)**i
        Opex_Batt.append(opex_annualise_Batt)

    ##TOTAL ----------------------------------

    CAPEX = Capex_WT + Capex_PV + Capex_Diesel + Capex_H2 + Capex_Batt
    OPEX = sum(Opex_WT) + sum(Opex_PV) + sum(Opex_Diesel) + sum(Opex_Batt) + sum(Opex_H2)
    TOTAL_EX = CAPEX + OPEX + CF * Generateur_diesel.fuel_cost
    TOTAL_NRJ_annuel = sum(load[:durée])
    TOTAL_NRJ = 0
    for j in range(Lifetime):
        TOTAL_NRJ += TOTAL_NRJ_annuel / (1 + Discount_rate)**j

    if TOTAL_NRJ == 0.0 :
        LCOE = 1e9
    else :
        LCOE = TOTAL_EX / TOTAL_NRJ    

    if données :
        rendu = (LCOE, CF, profile)
    else :
        rendu = (LCOE, CF)
        
    if graphique :
        # Affichage graphique
        print("Graphique à suivre")

    return rendu


simulation([2, 1, 2, 1, [1802, 544, 400]])

















