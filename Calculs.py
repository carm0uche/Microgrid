from Data import *
from Classes import *

PV_nb = None
WT_nb = None
Fuel_nb = None
H2_nb = None
Batt_nb = None

#Valeurs initiales batterie & H2
batt_init_value = 0.5 * Batterie.capacity
h2_init_value = 0.5 * Stockage_hydrogene.capacity

#profile = [Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage]
profile = [[0], [0], [0], [batt_init_value], [h2_init_value], [0], [0]]

def calcul_power_PV(i, current_profile):
    current_power = PV_nb * Panneau_solaire.power * ppvCf[i]
    current_profile[1] = [current_power] 
    return None

def calcul_power_WT(i, current_profile):
    current_power = WT_nb * Eolienne.P_v[i]
    current_profile[0] = [current_power]
    return None

def calcul_power_ENR(i):
    return WT_nb * Eolienne.P_v[i] + PV_nb * Panneau_solaire.power * ppvCf[i]

def balance(i):
    current_power_ENR = calcul_power_ENR(i)
    return [current_power_ENR >= load[i], current_power_ENR - load[i]]

def set_energy_batt(v, current_profile):
    if profile[3][-1] + v < 0.2*Batterie.capacity:
        print(f"Low battery at {date[i]}")
    if profile[3][-1] + v < 0:
        raise ValueError("Battery error : Energy level cannot be negative")
    current_set = min(profile[3][-1] + v, Batterie.capacity)
    if current_set == Batterie.capacity :
        set_energy_h2(profile[3][-1] + v - Batterie.capacity, current_profile)
    current_profile[3] = [current_set]
    return None

def set_energy_h2(v, current_profile):
    if profile[4][-1] + v < 0:
        raise ValueError("H2 error : Energy level cannot be negative")
    current_set = min(profile[4][-1] + v, Stockage_hydrogene.capacity)
    if current_set == Stockage_hydrogene.capacity :
        current_profile[5] = [profile[4][-1] + v - Stockage_hydrogene.capacity]
    current_profile[4] = [current_set]
    return None

def set_power_gen(v, current_profile):
    current_profile=[v] 

def dispatch(i):
    [allow, number] = balance(i)
    current_profile = [[0], [0], [0], [profile[3][-1]], [profile[4][-1]], [0], [0]]

    if allow :
        if profile[3][-1] < Batterie.capacity :

            '''charger la batterie'''
            if number <= Batterie.charge_pw_max : 
                set_energy_batt(number, current_profile)
                return current_profile
            
            '''charger la batterie et l'hydrogène'''
            set_energy_batt(Batterie.charge_pw_max, current_profile)
            set_energy_h2(number - Batterie.charge_pw_max, current_profile)
            return current_profile
        
        '''charger l'hydrogène'''
        if profile[4][-1] < Stockage_hydrogene.capacity:
            set_energy_h2(number, current_profile)
            return current_profile
        '''curtailment'''
        current_profile[5].append(number)
        return current_profile
    
    else :
        if profile[3][-1] > Batterie.state_charge_min * Batterie.capacity :

            '''utiliser la batterie'''
            if profile[3][-1] + number > Batterie.state_charge_min * Batterie.capacity :
                set_energy_batt(number, current_profile)
                return current_profile
            
            current_level = profile[3][-1]
            set_energy_batt(Batterie.state_charge_min * Batterie.capacity - current_level, current_profile)
            number = number +  current_level - Batterie.state_charge_min * Batterie.capacity 

        if profile[4][-1] > 0 :
            
            '''utiliser l'hydrogène'''
            if profile[4][-1] + number > 0 :
                set_energy_h2(number, current_profile)
                return current_profile
            
            current_level = profile[4][-1]
            set_energy_h2(- current_level, current_profile)
            number = number + current_level
        else : 
            '''allumer le générateur'''
            if number < Generateur_diesel.max_power : 
                set_power_gen(-number)
                return current_profile
            
        set_power_gen(Generateur_diesel.max_power)
        current_profile[6] = Generateur_diesel.max_power + number
        return current_profile

    
    
