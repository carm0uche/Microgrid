import csv
from Classes import *
import openpyxl
import sys

#Extraction données Excel
file_name = "Data_project.xlsx"  
wb = openpyxl.load_workbook(file_name, data_only = True)
sheet = wb.active  

#var = float(sheet["B5"].value) if sheet["B5"].value is not None else 0.0
#list_values = [sheet[f"C{i}"].value for i in range(4, 12)]

#Environment data

import csv

Lifetime = float(sheet["AA5"].value) if sheet["AA5"].value is not None else 0.0
Discount_rate = float(sheet["AA6"].value) if sheet["AA6"].value is not None else 0.0
date = []
load = []
ppvCf = []
temp = []
wind = []
n_lignes = 35065

with open("ouessant_data.csv", newline='', encoding='utf-8') as fichier_csv:
    lecteur = csv.reader(fichier_csv, delimiter=";")
    next(lecteur)

    for i, ligne in enumerate(lecteur):
        if i >= n_lignes:
            break
        date.append(ligne[0])
        load.append(float(ligne[1]))
        ppvCf.append(float(ligne[2]))
        temp.append(float(ligne[3]))
        wind.append(float(ligne[4]))

#PV

PV_Name = "Panneau solaire"
PV_Lifetime = float(sheet["G5"].value) if sheet["G5"].value is not None else 0.0
PV_Power = float(sheet["G6"].value) if sheet["G6"].value is not None else 0.0 
PV_Derating_factor = float(sheet["G11"].value) if sheet["G11"].value is not None else 0.0
print(PV_Derating_factor)
PV_CAPEX = float(sheet["G9"].value) if sheet["G9"].value is not None else 0.0
PV_OPEX = float(sheet["G8"].value) if sheet["G8"].value is not None else 0.0
PV_Efficiency = sheet["G13"].value if sheet["G13"].value is not None else 0.0 

Panneau_solaire = PV(PV_Name, PV_Lifetime, PV_Power, PV_Derating_factor, PV_CAPEX, PV_OPEX, PV_Efficiency)

#Éolien

W_Name = "Eolienne"
W_Lifetime = float(sheet["K5"].value) if sheet["K5"].value is not None else 0.0
W_Rated_power = float(sheet["K6"].value) if sheet["K6"].value is not None else 0.0 
W_CAPEX = float(sheet["K8"].value) if sheet["K8"].value is not None else 0.0
W_OPEX = float(sheet["K9"].value) if sheet["K9"].value is not None else 0.0
W_P_v = ["à remplir par Baptiste ce crack qui a dit qu'il s'en chargeait je certifie"]

Eolienne = WT(W_Name, W_Lifetime, W_Rated_power, W_CAPEX, W_OPEX, W_P_v)

#Diesel

D_Name = "Générateur diesel"
D_Lifetime = float(sheet["S5"].value) if sheet["S5"].value is not None else 0.0
D_Max_power = float(sheet["S6"].value) if sheet["S6"].value is not None else 0.0
D_CAPEX = float(sheet["S8"].value) if sheet["S8"].value is not None else 0.0
D_OPEX = float(sheet["S9"].value) if sheet["S9"].value is not None else 0.0
D_Salvage = float(sheet["S10"].value) if sheet["S10"].value is not None else 0.0
D_Max_use = float(sheet["S11"].value) if sheet["S11"].value is not None else 0.0
D_Fuel_cost = float(sheet["S13"].value) if sheet["S13"].value is not None else 0.0
D_Fuel_consumption = [[float(sheet[f"V{i}"].value) for i in range(5, 15)],[float(sheet[f"W{i}"].value) for i in range(5, 15)]]
D_Efficiency = [[float(sheet[f"V{i}"].value) for i in range(5, 15)],[float(sheet[f"x{i}"].value) for i in range(5, 15)]]

Generateur_diesel = Fuel(D_Name, D_Lifetime, D_Max_power, D_CAPEX, D_OPEX, D_Salvage, D_Max_use, D_Fuel_cost, D_Fuel_consumption, D_Efficiency)

#Hydrogène

H_Name = "Stockage hydrogène"
H_Lifetime = float(sheet["O5"].value) if sheet["O5"].value is not None else 0.0
H_Capacity = float(sheet["O6"].value) if sheet["O6"].value is not None else 0.0
H_Efficiency = float(sheet["O7"].value) if sheet["O7"].value is not None else 0.0
H_CAPEX_el = float(sheet["O9"].value) if sheet["O9"].value is not None else 0.0
H_OPEX_el = float(sheet["O10"].value) if sheet["O10"].value is not None else 0.0
H_CAPEX_tank = float(sheet["O11"].value) if sheet["O11"].value is not None else 0.0
H_OPEX_tank = float(sheet["O12"].value) if sheet["O12"].value is not None else 0.0
H_Salvage = float(sheet["O14"].value) if sheet["O14"].value is not None else 0.0
H_Max_start = float(sheet["O16"].value) if sheet["O16"].value is not None else 0.0
H_Max_use = float(sheet["O17"].value) if sheet["O17"].value is not None else 0.0

Stockage_hydrogene = Hydrogen(H_Name, H_Lifetime, H_Capacity, H_Efficiency, H_CAPEX_el, H_OPEX_el, H_CAPEX_tank, H_OPEX_tank, H_Salvage, H_Max_start, H_Max_use)

#Batteries

B_Name = "Batteries lithium"
B_Lifetime = float(sheet["C6"].value) if sheet["C6"].value is not None else 0.0
B_Capacity = float(sheet["C7"].value) if sheet["C7"].value is not None else 0.0
B_Efficiency = float(sheet["C12"].value) if sheet["C12"].value is not None else 0.0
B_CAPEX = float(sheet["C10"].value) if sheet["C10"].value is not None else 0.0
B_OPEX = float(sheet["C9"].value) if sheet["C9"].value is not None else 0.0
B_State_charge_min = float(sheet["C15"].value) if sheet["C15"].value is not None else 0.0
B_Thrpt = float(sheet["C5"].value) if sheet["C5"].value is not None else 0.0
B_Charge_pw_max = float(sheet["C13"].value) if sheet["C13"].value is not None else 0.0
B_Discharge_pw_max = float(sheet["C14"].value) if sheet["C14"].value is not None else 0.0

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




#fichier recap données

with open("recap_datas.txt", "w") as f:
    sys.stdout = f  # Redirige tous les prints vers le fichier
    print("-- PV --")
    Panneau_solaire.display_info()
    print()
    print("-- WT --")
    Eolienne.display_info()
    print()
    print("-- Fuel --")
    Generateur_diesel.display_info()
    print()
    print("-- H2 --")
    Stockage_hydrogene.display_info()
    print()
    print("-- Batt --")
    Batterie.display_info()

