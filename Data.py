import csv
from Classes import *
import openpyxl

#Extraction données Excel
file_name = "Data_project.xlsx"  
wb = openpyxl.load_workbook(file_name)
sheet = wb.active  

#var = float(sheet["B5"].value) if sheet["B5"].value is not None else 0.0
#list_values = [sheet[f"C{i}"].value for i in range(4, 12)]

#PV

PV_Name = "Panneau solaire"
PV_Lifetime = float(sheet["G5"].value) if sheet["G5"].value is not None else 0.0
PV_Power = float(sheet["G6"].value) if sheet["G6"].value is not None else 0.0 
PV_Derating_factor = float(sheet["G11"].value) if sheet["G11"].value is not None else 0.0
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
W_P_v = [[float(sheet[f"J{i}"].value) for i in range(18, 44)],[float(sheet[f"K{i}"].value) for i in range(18, 44)]]

Eolienne = WT(W_Name, W_Lifetime, W_Rated_power, W_CAPEX, W_OPEX, W_P_v)

#Diesel

D_Name = None
D_Lifetime = None
D_Max_power = None
D_CAPEX = None
D_OPEX = None
D_Salvage = None
D_Max_use = None
D_Fuel_cost = None
D_Fuel_consumption = None
D_Efficiency = None

Generateur_diesel = Fuel(D_Name, D_Lifetime, D_Max_power, D_CAPEX, D_OPEX, D_Salvage, D_Max_use, D_Fuel_cost, D_Fuel_consumption, D_Efficiency)

#Hydrogène

H_Name = None
H_Lifetime = None
H_Capacity = None
H_Efficiency = None
H_CAPEX_el = None
H_OPEX_el = None
H_CAPEX_tank = None
H_OPEX_tank = None
H_Salvage = None
H_Max_start = None
H_Max_use = None

Stockage_hydrogene = Hydrogen(H_Name, H_Lifetime, H_Capacity, H_Efficiency, H_CAPEX_el, H_OPEX_el, H_CAPEX_tank, H_OPEX_tank, H_Salvage, H_Max_start, H_Max_use)

#Batteries

B_Name = None
B_Lifetime = None
B_Capacity = None
B_Efficiency = None
B_CAPEX = None
B_OPEX = None
B_State_charge_min = None
B_Thrpt = None
B_Charge_pw_max = None
B_Discharge_pw_max = None

Batterie = Batt(B_Name, B_Lifetime, B_Capacity, B_Efficiency, B_CAPEX, B_OPEX, B_State_charge_min, B_Thrpt, B_Charge_pw_max, B_Discharge_pw_max)
                
#Environment data

import csv

Lifetime = None
Discount_rate = None
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




tracer_load_5_ans(date, load, fenetre_moyenne=24*7)
