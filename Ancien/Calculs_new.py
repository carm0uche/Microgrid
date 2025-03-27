from Nouveau.Data import *
from Nouveau.Classes import *
from tqdm import tqdm

#leviers d'optimisation
#param = [PV_nb, WT_nb, Fuel_nb, H2_nb, Batt_nb]

def dispatch(i, profile, param):
    print(i)
    current_profile = [[0], [0], [0], [profile[3][-1]], [profile[4][-1]], [0], [0]]

    #calcul puissance PV
    def calcul_PV() :
        return [param[0] * Panneau_solaire.power * ppvCf[i]]
    
    #calcul puissance WT
    def calcul_WT():
        return [param[1] * Eolienne.P_v[i]]
        
    #calcul puissance totale ENR
    def calcul_power_ENR():
        return calcul_PV()[0] + calcul_WT()[0]
    
    #calcul balance production/besoins
    def balance():
        current_power_ENR = calcul_power_ENR()
        return [current_power_ENR >= load[i], current_power_ENR - load[i]]
    
    #calcul énergie batterie
    def set_energy_batt(v):
        current_set = min(profile[3][-1] + v, Batterie.capacity * param[4])
        if current_set == Batterie.capacity * param[4] :
            current_profile[4] = set_energy_h2(profile[3][-1] + v - Batterie.capacity * param[4])
        return [current_set]
    
    #calcul énergie h2
    def set_energy_h2(v):
        current_set = min(profile[4][-1] + v, Stockage_hydrogene.capacity * param[3])
        if current_set == Stockage_hydrogene.capacity * param[3] :
            current_profile[5] = [profile[4][-1] + v - Stockage_hydrogene.capacity * param[3]]
        return [current_set]
    
    #dispatch
    [allow, number] = balance()

    current_profile[0] = calcul_WT()
    current_profile[1] = calcul_PV()
    print("jour :", i)
    print("charge : ", load[0])
    print("PV :", current_profile[1], "WT :", current_profile[0], "Somme :", current_profile[0]+current_profile[1])
    print(allow)
    if allow :
        print("allow = true")

        print("batterie capacity :", profile [3][-1], "<", Batterie.capacity * param[4])
        if profile[3][-1] < Batterie.capacity * param[4] :
            print(True)
            '''charger la batterie'''

            print("puissance max de charge :", number ,"<=", Batterie.charge_pw_max * param[4] )
            if number <= (Batterie.charge_pw_max * param[4])/Batterie.efficiency :
                print(True) 
                current_profile[3] = set_energy_batt(Batterie.efficiency * number)
                return current_profile
            print(False)
            '''charger la batterie et l'hydrogène'''
            print("puissance de charge dépassée, charge max :", Batterie.charge_pw_max * param[4])
            current_profile[3] = set_energy_batt(Batterie.charge_pw_max * param[4])
            current_profile[4][0] += set_energy_h2(number - Batterie.charge_pw_max * param[4] / Batterie.efficiency)[0]
            return current_profile
        
        '''charger l'hydrogène'''
        print("charge h2 :",profile[4][-1]," <", Stockage_hydrogene.capacity * param[3])
        if profile[4][-1] < Stockage_hydrogene.capacity * param[3]:
            print(True)
            print("charge h2 :", number)
            current_profile[4] = set_energy_h2(number * Stockage_hydrogene.efficiency)
            return current_profile
        
        print(False)
        '''curtailment'''
        print("curtailment :", number)
        current_profile[5] = [number]
        return current_profile
    
    else :
        print("allow = False")
        print("Reste de la batterie :", profile[3][-1], ">", Batterie.state_charge_min * Batterie.capacity * param[4] )
        if profile[3][-1] > Batterie.state_charge_min * Batterie.capacity * param[4] :
            
            print(True)
            '''utiliser la batterie'''
            print("Que de la batterie :",profile[3][-1] + number ,">", Batterie.state_charge_min * Batterie.capacity * param[4] )
            if profile[3][-1] + number > Batterie.state_charge_min * Batterie.capacity * param[4] :
                print(True)
                current_profile[3] = set_energy_batt(number)
                return current_profile
            
            print(False)
            current_level = profile[3][-1]
            print("niveau de batterie :", current_level)
            print("demande :", number)
            print("utilisation de la batterie à hauteur de: ",Batterie.state_charge_min * Batterie.capacity * param[4] - current_level) 
            current_profile[3] = set_energy_batt(Batterie.state_charge_min * Batterie.capacity * param[4] - current_level)
            number = number +  current_level - Batterie.state_charge_min * Batterie.capacity * param[4]

        
        print("Reste à combler :", number)
    
        print("Reste d'hydrogène :", profile[4][-1]," >", 0 )
        if profile[4][-1] > 0 :
            print(True)
            '''utiliser l'hydrogène'''
            print("Suffisemment d'h2 :", profile[4][-1] + number," >", 0 )
            if profile[4][-1] + number > 0 :
                print(True)
                current_profile[4] = set_energy_h2(number)
                return current_profile
            print(False)

            current_level = profile[4][-1]
            print("niveau d'H2 :",current_level )
            print("demande :", number)
            current_profile[4] = set_energy_h2(- current_level)
            number = number + current_level
            print("reste à combler :", number)

        
        print(False) 
        '''allumer le générateur'''
        print("Assez de puissance fuel :", -number, "<", Generateur_diesel.max_power * param[2] )
        if -number < Generateur_diesel.max_power * param[2] : 
            print(True)
            current_profile[2] = [-number]
            return current_profile
        print(False)

        current_profile[2] = [Generateur_diesel.max_power * param[2]]
        current_profile[6] = [Generateur_diesel.max_power * param[2] + number]
        print("Shortage :", Generateur_diesel.max_power * param[2] + number)
        return current_profile
    
def heure_de_plus(i, profile, params) : 
    #print("heure :", i)
    #print("paramètres :", params)
    #print("load :", load[i])
    #print("[",profile[0][-1], profile[1][-1], profile[2][-1], profile[3][-1], profile[4][-1], profile[5][-1], profile[6][-1], "]")
    
    current_profile = dispatch(i, profile, params)
    if i>0 :
        for j in range(len(current_profile)):
            profile[j] += current_profile[j]
        return profile
    return current_profile

def calcul_simu(params):

    #Valeurs initiales batterie & H2
    batt_init_value = 0.5 * Batterie.capacity * params[4]
    h2_init_value = 0.5 * Stockage_hydrogene.capacity * params[3]

    #profile = [Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage]
    profile0 = [[0], [0], [0], [batt_init_value], [h2_init_value], [0], [0]]

    profile = heure_de_plus(0, profile0, params)
    for k in range(1,24) :
        heure_de_plus(k, profile, params)
        #print("load :", load[k])
        #print(profile)
        print(k)
    return profile

calcul_simu([2000,1,1,10,10])

#for i in tqdm(range(100), desc="Simulation en cours", unit="it"):   
    #profile = heure_de_plus(0)

    #for k in range(1,n_lignes) :
     #heure_de_plus(k,profile)
    
    #print("Fin de la simulation.")
