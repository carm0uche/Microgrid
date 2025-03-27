from scipy.optimize import shgo
from Simu_final import *
from tqdm import tqdm
from scipy.optimize import dual_annealing

pbar = tqdm(total=10000)

def objective(params):
    #print(params)
    
    params_entiers = [int(k) + 1 for k in params]
    #print(params_entiers)

    pbar.update(1)
    
    LCOE, conso_fuel, profile = simulation(params_entiers)

    shortage = sum(profile[-1])

    # Pénalité massive si le shortage > 0
    if shortage > 0:
        return 1e9  # Une valeur énorme pour rendre cette solution non viable

    # Fonction de coût pondérée
    lambda_weight = 1e-6  # Pondération écologique (modifiable)
    
    return LCOE + lambda_weight * conso_fuel

print("Simulation en cours...")
bounds = [
    (0,6),   # Nombre d'éolienne
    (0,5000),  # Nombre de PV
    (0,5), # Nombre de générateurs diesel
    (0,100), # Nombre de batteries
    (0, 2000)]   # Nombre d'électrolyseur 



# Exécution de l'optimisation bayésienne
#result = shgo(objective, bounds, n=300, options={"maxiter": 500, "itermin": 20, "disp": True, "ftol": 1e-3} , sampling_method='simplicial')
result = dual_annealing(objective, bounds, maxiter = 1000)
pbar.close()

# Résultats
best_x = result.x
best_x_entier = [int(k) + 1 for k in best_x]

print("Meilleure config :", best_x)
print("Meilleure config entière :", best_x_entier)
print("Meilleur score :", result.fun)
