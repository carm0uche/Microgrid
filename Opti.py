from scipy.optimize import shgo
import numpy as np
from Calculs_new import *
from calcul_LCOE import *
from Simulation_new import *
from tqdm import tqdm
from skopt import gp_minimize
from skopt.space import Integer

def objective(params):
    #print(params)

    #params_entiers = [int(k) for k in params]
    #print(params_entiers)
    # Appel du simulateur (à remplacer par la vraie fonction)
    LCOE, carbone, shortage = simulation_microgrid(params)

    # Pénalité massive si le shortage > 0
    if shortage > 0:
        return 1e9  # Une valeur énorme pour rendre cette solution non viable

    # Fonction de coût pondérée
    lambda_weight = 10  # Pondération écologique (modifiable)
    
    return LCOE + lambda_weight * carbone

# Définition de l'espace de recherche
bounds = [
    (0,10000), #Taille batterie (kWh) 
    (0,5000),  # Puissance PV (kW)
    (0,5000),   # Puissance éolienne (kW)
    (0, 2000),   # Puissance électrolyseur (kW) 
    (0, 2000),   # Puissance pile à combustible (kW)
    (0, 1000)]   # Taille du réservoir d'hydrogène (m^3) 


print("Simulation en cours...")
# Exécution de l'optimisation bayésienne
#result = shgo(objective, bounds, n=500, options={"maxiter": 1000, "itermin": 5, "disp": True, "ftol": 1e-2}, sampling_method='simplicial')
result = gp_minimize(objective, bounds, n_calls=100, random_state=42)


# Résultats
best_x = result.x
#best_x_entier = [int(k) + 1 for k in best_x]

print("Meilleure config :", best_x)
#print("Meilleure config entière :", best_x_entier)
print("Meilleur score :", result.fun)
#print("Nombre total d'évaluations de la fonction objective :", result.nfev)
#print("Nombre total d'itérations de SHGO :", result.nit)

