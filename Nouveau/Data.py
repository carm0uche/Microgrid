from Classes import *
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import sys

import os
print(os.getcwd())

print("Extraction des données...")
n_lignes = 35064  # Nombre de lignes à charger
date = []
load = []
ppvCf = []
temp = []
wind = []

# Charger le CSV avec pandas
df = pd.read_csv("Nouveau\ouessant_data.csv", delimiter=";", encoding="utf-8", nrows=n_lignes)

# Extraire les colonnes sous forme de listes
date = df.iloc[:, 0].tolist()
load = df.iloc[:, 1].astype(float).tolist()
ppvCf = df.iloc[:, 2].astype(float).tolist()
temp = df.iloc[:, 3].astype(float).tolist()
wind = df.iloc[:, 4].astype(float).tolist()

# Charger les données Excel avec pandas
file_name = "Nouveau\Data_project.xlsx"
df_excel = pd.read_excel(file_name, sheet_name=0, header=None)

Lifetime = int(df_excel.iloc[4, 26]) if pd.notna(df_excel.iloc[4, 26]) else 0
Discount_rate = df_excel.iloc[5, 26] if pd.notna(df_excel.iloc[5, 26]) else 0.0

# Extraction des données Excel
PV_Name = "Panneau solaire"
PV_Lifetime = df_excel.iloc[4, 6] if pd.notna(df_excel.iloc[4, 6]) else 0.0
PV_Power = df_excel.iloc[5, 6] if pd.notna(df_excel.iloc[5, 6]) else 0.0
PV_Derating_factor = df_excel.iloc[10, 6] if pd.notna(df_excel.iloc[10, 6]) else 0.0
PV_CAPEX = df_excel.iloc[8, 6] if pd.notna(df_excel.iloc[8, 6]) else 0.0
PV_OPEX = df_excel.iloc[7, 6] if pd.notna(df_excel.iloc[7, 6]) else 0.0
PV_Efficiency = df_excel.iloc[12, 6] if pd.notna(df_excel.iloc[12, 6]) else 1.0

W_Name = "Éolienne"
W_Lifetime = df_excel.iloc[4, 10] if pd.notna(df_excel.iloc[4, 10]) else 0.0
W_Rated_power = df_excel.iloc[5, 10] if pd.notna(df_excel.iloc[5, 10]) else 0.0
W_CAPEX = df_excel.iloc[7, 10] if pd.notna(df_excel.iloc[7, 10]) else 0.0
W_OPEX = df_excel.iloc[8, 10] if pd.notna(df_excel.iloc[8, 10]) else 0.0

df_excel_wind = pd.read_excel(file_name, sheet_name="full_data", header=0)

# Initialiser la liste pour stocker les puissances interpolées
W_P_v = []

# Données pour l'interpolation
d_vitesses = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 25.1, 26])
d_puissances = np.array([0, 0, 0, 7, 30, 69, 124, 201, 308, 439, 559, 698, 797, 859, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 0, 0])
interpolateur = interp1d(d_vitesses, d_puissances, kind='linear', fill_value="extrapolate")

# Boucle pour calculer les puissances interpolées
for i in range(n_lignes):
    wind = (float(df_excel_wind.iloc[i, 4]) if pd.notna(df_excel_wind.iloc[i, 4]) else 0.0) * (50/3)**0.1
    W_P_v.append(float(interpolateur(wind)))

D_Name = "Générateur diesel"
D_Lifetime = df_excel.iloc[4, 18] if pd.notna(df_excel.iloc[4, 18]) else 0.0
D_Max_power = df_excel.iloc[5, 18] if pd.notna(df_excel.iloc[5, 18]) else 0.0
D_CAPEX = df_excel.iloc[7, 18] if pd.notna(df_excel.iloc[7, 18]) else 0.0
D_OPEX = df_excel.iloc[8, 18] if pd.notna(df_excel.iloc[8, 18]) else 0.0
D_Salvage = df_excel.iloc[9, 18] if pd.notna(df_excel.iloc[9, 18]) else 0.0
D_Max_use = df_excel.iloc[10, 18] if pd.notna(df_excel.iloc[10, 18]) else 0.0
D_Fuel_cost = df_excel.iloc[12, 18] if pd.notna(df_excel.iloc[12, 18]) else 0.0

H_Name = "Stockage Hydrogène"
H_Lifetime = df_excel.iloc[4, 14] if pd.notna(df_excel.iloc[4, 14]) else 0.0
H_Capacity = df_excel.iloc[5, 14] if pd.notna(df_excel.iloc[5, 14]) else 0.0
H_Efficiency = [df_excel.iloc[6, 14] if pd.notna(df_excel.iloc[6, 14]) else 1.0, df_excel.iloc[7, 14] if pd.notna(df_excel.iloc[7, 14]) else 1.0]
H_CAPEX_el = df_excel.iloc[8, 14] if pd.notna(df_excel.iloc[8, 14]) else 0.0
H_OPEX_el = df_excel.iloc[9, 14] if pd.notna(df_excel.iloc[9, 14]) else 0.0
H_CAPEX_tank = df_excel.iloc[10, 14] if pd.notna(df_excel.iloc[10, 14]) else 0.0
H_OPEX_tank = df_excel.iloc[11, 14] if pd.notna(df_excel.iloc[11, 14]) else 0.0
H_CAPEX_fc = df_excel.iloc[18, 14] if pd.notna(df_excel.iloc[18, 14]) else 0.0
H_OPEX_fc = df_excel.iloc[19, 14] if pd.notna(df_excel.iloc[19, 14]) else 0.0
H_Salvage = df_excel.iloc[13, 14] if pd.notna(df_excel.iloc[13, 14]) else 0.0
H_Max_start = df_excel.iloc[15, 14] if pd.notna(df_excel.iloc[15, 14]) else 0.0
H_Max_use = df_excel.iloc[16, 14] if pd.notna(df_excel.iloc[16, 14]) else 0.0
H_charge_pw_max = df_excel.iloc[14, 14] if pd.notna(df_excel.iloc[14, 14]) else 1.0

B_Name = "Batterie lithium"
B_Lifetime = df_excel.iloc[5, 2] if pd.notna(df_excel.iloc[5, 2]) else 0.0
B_Capacity = df_excel.iloc[6, 2] if pd.notna(df_excel.iloc[6, 2]) else 0.0
B_Efficiency = df_excel.iloc[11, 2] if pd.notna(df_excel.iloc[11, 2]) else 0.0
B_CAPEX = df_excel.iloc[9, 2] if pd.notna(df_excel.iloc[9, 2]) else 0.0
B_OPEX = df_excel.iloc[8, 2] if pd.notna(df_excel.iloc[8, 2]) else 0.0
B_State_charge_min = df_excel.iloc[14, 2] if pd.notna(df_excel.iloc[14, 2]) else 0.0
B_Thrpt = df_excel.iloc[4, 2] if pd.notna(df_excel.iloc[4, 2]) else 0.0
B_Charge_pw_max = df_excel.iloc[12, 2] if pd.notna(df_excel.iloc[12, 2]) else 0.0
B_Discharge_pw_max = df_excel.iloc[13, 2] if pd.notna(df_excel.iloc[13, 2]) else 0.0

# Création des objets
Panneau_solaire = PV(PV_Name, PV_Lifetime, PV_Power, PV_Derating_factor, PV_CAPEX, PV_OPEX, PV_Efficiency)
Eolienne = WT(W_Name, W_Lifetime, W_Rated_power, W_CAPEX, W_OPEX, W_P_v)
Generateur_diesel = Fuel(D_Name, D_Lifetime, D_Max_power, D_CAPEX, D_OPEX, D_Salvage, D_Max_use, D_Fuel_cost)
Stockage_hydrogene = Hydrogen(H_Name, H_Lifetime, H_Capacity, H_Efficiency, H_CAPEX_el, H_OPEX_el, H_CAPEX_tank, H_OPEX_tank, H_CAPEX_fc, H_OPEX_fc, H_Salvage, H_Max_start, H_Max_use, H_charge_pw_max)
Batterie = Batt(B_Name, B_Lifetime, B_Capacity, B_Efficiency, B_CAPEX, B_OPEX, B_State_charge_min, B_Thrpt, B_Charge_pw_max, B_Discharge_pw_max)


import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def tracer_load_5_ans(date, load, fenetre_moyenne=24*7):
    """
    Trace la charge électrique demandée (Load) en MW sur les 5 premières années avec une moyenne hebdomadaire.

    :param date: Liste des dates sous format "12/01/2013 17:00"
    :param load: Charge électrique demandée en kW (sera convertie en MW)
    :param fenetre_moyenne: Nombre de points à moyenner (168 pour une moyenne hebdomadaire, car 24*7 = 168h)
    """
    # Convertir les dates en datetime
    dates_dt = [datetime.strptime(d, "%d/%m/%Y %H:%M") for d in date]

    # Déterminer la première année et la période des 5 ans
    premiere_annee = dates_dt[0].year
    derniere_annee = premiere_annee + 5

    # Filtrer les données sur les 5 premières années
    indices_5_ans = [i for i, d in enumerate(dates_dt) if premiere_annee <= d.year < derniere_annee]
    dates_filtres = [dates_dt[i] for i in indices_5_ans]
    load_filtree = [load[i] / 1000 for i in indices_5_ans]  # kW -> MW

    # Appliquer une moyenne glissante hebdomadaire (168h)
    load_moyenne = np.convolve(load_filtree, np.ones(fenetre_moyenne)/fenetre_moyenne, mode='valid')

    # Réduire aussi le nombre de dates pour correspondre aux valeurs moyennées
    dates_moyenne = dates_filtres[:len(load_moyenne)]

    # Tracé du graphique
    plt.figure(figsize=(14, 6))
    plt.plot(dates_moyenne, load_moyenne, label="Charge électrique (moyenne hebdomadaire)", color='b')

    plt.xlabel("Temps")
    plt.ylabel("Charge (MW)")
    plt.title(f"Évolution de la charge électrique - {premiere_annee}-{derniere_annee-1}")
    plt.legend()
    
    # Réduction du nombre de labels sur l'axe X (un label tous les ~6 mois)
    plt.xticks(dates_moyenne[::26*7*24], rotation=45)  # 26 semaines ≈ 6 mois

    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

print("Succès.")
#fichier recap données

#with open("recap_datas.txt", "w") as f:
    #sys.stdout = f  # Redirige tous les prints vers le fichier
    #print("-- PV --")
    #Panneau_solaire.display_info()
    #print()
    #print("-- WT --")
    #Eolienne.display_info()
    #print()
    #print("-- Fuel --")
    #Generateur_diesel.display_info()
    #print()
    #print("-- H2 --")
    #Stockage_hydrogene.display_info()
    #print()
    #print("-- Batt --")
    #Batterie.display_info()


