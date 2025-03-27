from scipy.optimize import shgo
from Simu_final import *
from tqdm import tqdm
from scipy.optimize import dual_annealing

print("Simulation en cours...")
pbar = tqdm(total=17705)

def objective(params):
    #print(params)
    paramètres = [int(params[0]) + 1, int(params[1]) + 1, int(params[2]), int(params[3]) + 1, [int(params[4]) + 1, params[5], params[6]]]
    #print(paramètres)
    pbar.update(1)
    
    LCOE, conso_fuel, profile = simulation(paramètres)

    shortage = sum(profile[-1])

    # Pénalité massive si le shortage > 0
    if shortage > 0:
        return 1e9  

    # Fonction de coût pondérée
    lambda_weight = 1e-6  # Pondération écologique (modifiable)
    
    return LCOE

bounds = [
    (0, 5),   # Nombre d'éolienne
    (0, 7500),  # Nombre de PV
    (0, 2), # Nombre de générateurs diesel
    (0, 100), # Nombre de batteries
    (0, 10000), # Nombre de stockage h2 
    (0, 2000), # Puissance électrolyseur
    (0, 2000)]   # Puissance pile à combustible

# Exécution de l'optimisation bayésienne
#result = shgo(objective, bounds, n=300, options={"maxiter": 500, "itermin": 20, "disp": True, "ftol": 1e-3} , sampling_method='simplicial')
result = dual_annealing(objective, bounds, maxiter = 2000, seed = 1, minimizer_kwargs={"tol":1e-3})
pbar.close()

# Résultats
best_x = result.x
best_x_entier = [int(k) + 1 for k in best_x]

print("Meilleure config :", best_x)
print("Meilleure config entière :", best_x_entier)
print("Meilleur score :", result.fun)
print("Raison :", result.message)
