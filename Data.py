import csv
from Classes import *
import openpyxl

#file_name = "datas.xlsx"  
#wb = openpyxl.load_workbook(file_name)
#sheet = wb.active  

#var = sheet["B5"].value

#list_values = [sheet[f"C{i}"].value for i in range(4, 12)]

#PV

PV_Name = None
PV_Lifetime = None
PV_Power = None 
PV_Derating_factor = None
PV_CAPEX = None
PV_OPEX = None
PV_Efficiency = None 

Panneau_solaire = PV(PV_Name, PV_Lifetime, PV_Power, PV_Derating_factor, PV_CAPEX, PV_OPEX, PV_Efficiency)

#Éolien

W_Name = None
W_Lifetime = None
W_Rated_power = None 
W_CAPEX = None
W_OPEX = None
W_P_v = None

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

