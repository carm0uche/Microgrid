from Data import *
from Classes import *

#leviers d'optimisation
#param = [PV_nb, WT_nb, Fuel_nb, H2_nb, Batt_nb]
param = [0, 0, 0, 0, 0, 0]

#Valeurs initiales batterie & H2
batt_init_value = 0.5 * Batterie.capacity
h2_init_value = 0.5 * Stockage_hydrogene.capacity

#profile = [Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage]
profile0 = [[0], [0], [0], [batt_init_value], [h2_init_value], [0], [0]]

def dispatch(i, profile = profile0, param = param, batt0 = batt_init_value, h20 = h2_init_value):

    current_profile = [[0], [0], [0], profile[3][-1], profile[4][-1], [0], [0]]

    #calcul puissance PV
    def calcul_PV() :
        return [PV_nb * Panneau_solaire.power * ppvCf[i]]
    
    #calcul puissance WT
    def calcul_WT():
        return [WT_nb * Eolienne.P_v[i]]
        
    #calcul puissance totale ENR
    def calcul_power_ENR():
        return calcul_PV() + calcul_WT()
    
    #calcul balance production/besoins
    def balance():
        current_power_ENR = calcul_power_ENR()
        return [current_power_ENR >= load[i], current_power_ENR - load[i]]
    
    #calcul énergie batterie
    def set_energy_batt(v):
        current_set = min(profile[3][-1] + v, Batterie.capacity)
        if current_set == Batterie.capacity :
            current_profile[4] = set_energy_h2(profile[3][-1] + v - Batterie.capacity)
        return [current_set]
    
    #calcul énergie h2
    def set_energy_h2(v):
        current_set = min(profile[4][-1] + v, Stockage_hydrogene.capacity)
        if current_set == Stockage_hydrogene.capacity :
            current_profile[5] = [profile[4][-1] + v - Stockage_hydrogene.capacity]
        return [current_set]
    
    #dispatch
    [allow, number] = balance(i)

    current_profile[0] = calcul_WT()
    current_profile[1] = calcul_PV()

    if allow :
        if profile[3][-1] < Batterie.capacity :

            '''charger la batterie'''
            if number <= Batterie.charge_pw_max : 
                current_profile[3] = set_energy_batt(number)
                return current_profile
            
            '''charger la batterie et l'hydrogène'''
            current_profile[3] = set_energy_batt(Batterie.charge_pw_max)
            current_profile[4][0] += set_energy_h2(number - Batterie.charge_pw_max)[0]
            return current_profile
        
        '''charger l'hydrogène'''
        if profile[4][-1] < Stockage_hydrogene.capacity:
            current_profile = set_energy_h2(number)
            return current_profile
        
        '''curtailment'''
        current_profile[5] = [number]
        return current_profile
    
    else :
        if profile[3][-1] > Batterie.state_charge_min * Batterie.capacity :

            '''utiliser la batterie'''
            if profile[3][-1] + number > Batterie.state_charge_min * Batterie.capacity :
                current_profile[3] = set_energy_batt(number)
                return current_profile
            
            current_level = profile[3][-1]
            current_profile[3] = set_energy_batt(Batterie.state_charge_min * Batterie.capacity - current_level)
            number = number +  current_level - Batterie.state_charge_min * Batterie.capacity 

        if profile[4][-1] > 0 :
            
            '''utiliser l'hydrogène'''
            if profile[4][-1] + number > 0 :
                current_profile[4] = set_energy_h2(number)
                return current_profile
            
            current_level = profile[4][-1]
            current_profile[4] = set_energy_h2(- current_level)
            number = number + current_level

        else : 
            '''allumer le générateur'''
            if -number < Generateur_diesel.max_power : 
                current_profile[2] = [-number]
                return current_profile
            
        current_profile[2] = [Generateur_diesel.max_power]
        current_profile[6] = Generateur_diesel.max_power + number
        return current_profile
    
def jour_de_plus(i, profile) : 

    if i == 0 :
        current_profile = dispatch(i)
    else :
        current_profile = dispatch(i, profile)
    
    for j in range(len(current_profile)):
        profile[j] += current_profile[j]
    
    return profile



