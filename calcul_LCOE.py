from Data import *

def calcul_LCOE_simu(params, simulation):

    ## PV ------------------------
    
    Capex_PV = Panneau_solaire.capex * Panneau_solaire.power * params[0]
    Opex_PV = []
    opex_annuel_PV = Panneau_solaire.power * Panneau_solaire.opex * params[0]

    for i in range(Lifetime) : 
        opex_annualise_PV = opex_annuel_PV/(1+Discount_rate)**i
        Opex_PV.append(opex_annualise_PV)

    ## WT ------------------------

    Capex_WT = Eolienne.capex * Eolienne.rated_power * params[1]
    Opex_WT = []
    opex_annuel_WT = Eolienne.rated_power * Eolienne.opex * params[1]

    for i in range(Lifetime) : 
        opex_annualise_WT = opex_annuel_WT/(1+Discount_rate)**i
        Opex_WT.append(opex_annualise_WT)

    ## Diesel ------------------------

    Capex_Diesel = Generateur_diesel.capex * Generateur_diesel.max_power * params[2]
    Opex_Diesel = []
    opex_annuel_Diesel = Generateur_diesel.max_power * Generateur_diesel.opex * params[2]

    for i in range(Lifetime) : 
        opex_annualise_Diesel = opex_annuel_Diesel/(1+Discount_rate)**i
        Opex_Diesel.append(opex_annualise_Diesel)

    ## H2 -------------------------------- //à compléter//

    Capex_H2 = (Stockage_hydrogene.capacity * Stockage_hydrogene.capex_tank / 33,3 + Stockage_hydrogene.charge_pw_max * Stockage_hydrogene.capex_el) * params[3] 
    Opex_H2 = []
    opex_annuel_H2 = (Stockage_hydrogene.storage * Stockage_hydrogene.opex_tank + Stockage_hydrogene.capacity*Stockage_hydrogene.opex_el) * params[3]

    for i in range(Lifetime) : 
        opex_annualise_H2 = opex_annuel_H2/(1+Discount_rate)**i
        Opex_H2.append(opex_annualise_H2)

    ## Batt ------------------------------

    Capex_Batt = Batterie.capex * Batterie.capacity * params[4]
    Opex_Batt = []
    opex_annuel_Batt = Batterie.capacity * Batterie.opex * params[4]

    for i in range(Lifetime) : 
        opex_annualise_Batt = opex_annuel_Batt/(1+Discount_rate)**i
        Opex_Batt.append(opex_annualise_Batt)

    ##TOTAL ----------------------------------

    CAPEX = Capex_WT + Capex_PV + Capex_Diesel + Capex_H2 + Capex_Batt
    OPEX = sum(Opex_WT) + sum(Opex_PV) + sum(Opex_Diesel) + sum(Opex_Batt)
    TOTAL_EX = CAPEX + OPEX

    TOTAL_NRJ = sum(simulation[0]) + sum(simulation[1])

    if TOTAL_NRJ == 0.0 :
        return 1e9
    
    return TOTAL_EX / TOTAL_NRJ



