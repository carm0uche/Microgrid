from skopt import gp_minimize
from skopt.space import Integer
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
space = [
    Integer(0, 100, name="n_pv"),  # Exemple : entre 0 et 100 panneaux PV
    Integer(0, 5, name="n_wt"),   # Éoliennes
    Integer(0, 5, name="n_gen"),  # Générateurs
    Integer(0, 50, name="n_h2"),   # Stockage hydrogène
    Integer(0, 100, name="n_batt") # Batteries
]

# Exécution de l'optimisation bayésienne
result = gp_minimize(objective, space, n_calls=50, random_state=42)

# Résultats
print("Meilleure config :", result.x)
print("Meilleur score :", result.fun)
