from skopt import gp_minimize
from skopt.space import Integer
pip install scipy
from scipy.optimize import shgo
import numpy as np
from Calculs_new import *
from calcul_LCOE import *
from Simulation import *

def objective(params):

    # Appel du simulateur (à remplacer par la vraie fonction)
    LCOE, carbone, shortage = simulation_microgrid(params)

    # Pénalité massive si le shortage > 0
    if shortage > 0:
        return 1e6  # Une valeur énorme pour rendre cette solution non viable

    # Fonction de coût pondérée
    lambda_weight = 10  # Pondération écologique (modifiable)
    return LCOE + lambda_weight * carbone


# Définition de l'espace de recherche
bounds = [
    (0,10000), #Taille batterie 
    (0,5000),  # Puissance PV
    (0,5000),   # Puissance éolienne
    (0, 2000),   # Puissance électrolyseur
    (0, 2000),   # Puissance pile à combustible
    (0, 1000)]   # Taille du réservoir d'hydrogène
]

# Exécution de l'optimisation bayésienne
result = shgo(objective, bounds, n=500, options={"maxiter": 1000, "itermin": 20, "disp": True, "ftol": 1e-4})

# Résultats
print("Meilleure config :", result.x)
print("Meilleur score :", result.fun)
