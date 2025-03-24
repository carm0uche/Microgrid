from Classes import *

PV_nb = None
WT_nb = None
Fuel_nb = None
H2_nb = None
Batt_nb = None

#Valeurs initiales batterie & H2
batt_init_value = 0
h2_init_value = 0

#profile = [Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage]
profile = [[], [], [], [], [], [], []]

import numpy as np
from scipy.optimize import minimize

def lcoe(params, *args):
    # Extraire les paramètres du vecteur
    battery_size, pv_power, wind_power, electrolyzer_power, fuel_cell_power, hydrogen_tank_size = params
    
    # Coefficients de coût (exemples, à ajuster selon le modèle)
    c_battery = 500  # Coût par kWh de batterie
    c_pv = 1000  # Coût par kW de PV
    c_wind = 1200  # Coût par kW éolien
    c_electrolyzer = 1500  # Coût par kW électrolyseur
    c_fuel_cell = 1000  # Coût par kW pile à combustible
    c_hydrogen_tank = 200  # Coût par m3 de réservoir d'hydrogène
    
    # Calcul du CAPEX
    capex = (c_battery * battery_size + c_pv * pv_power + c_wind * wind_power +
             c_electrolyzer * electrolyzer_power + c_fuel_cell * fuel_cell_power + c_hydrogen_tank * hydrogen_tank_size)
    
    # Calcul de l'OPEX (par exemple, 2% du CAPEX)
    opex = 0.02 * capex
    
    # Calcul de la production d'énergie (simplifié)
    # Hypothèses sur les heures de production par an et l'efficacité des systèmes
    hours_pv = 1500  # Heures de production par an (par exemple)
    hours_wind = 2000
    efficiency_electrolyzer = 0.7
    efficiency_fuel_cell = 0.6
    
    E_pv = pv_power * hours_pv
    E_wind = wind_power * hours_wind
    E_hydrogen = (electrolyzer_power * efficiency_electrolyzer * fuel_cell_power * efficiency_fuel_cell)
    
    # Production totale d'énergie
    E_total = E_pv + E_wind + E_hydrogen
    
    # Calcul du LCOE
    lcoe_value = (capex + opex) / E_total
    return lcoe_value

# Définir des limites pour les variables d'optimisation
bounds = [(0, 10000),  # Taille de la batterie
          (0, 5000),   # Puissance photovoltaïque
          (0, 5000),   # Puissance éolienne
          (0, 2000),   # Puissance électrolyseur
          (0, 2000),   # Puissance pile à combustible
          (0, 1000)]   # Taille du réservoir d'hydrogène

# Exemple d'appel à l'optimiseur scipy
initial_guess = [500, 1000, 1000, 500, 500, 100]  # Valeurs initiales
result = minimize(lcoe, initial_guess, bounds=bounds)
print(f"Solution optimale: {result.x}")
print(f"LCOE optimal: {result.fun}")


