# Description: Calcul du LCOE pour un microgrid
from Data import *

import csv
from Classes import *
import openpyxl

#Extraction données Excel
file_name = "Data_project.xlsx"  
wb = openpyxl.load_workbook(file_name, data_only = True)
sheet = wb.active  



##Capex  
#n_PV = ? # nombre de panneaux solaires installés
#n_WT = ? # nombre d'éoliennes installées
#n_batterie = ? # nombre de batteries installées
#n_hydrogene = ? # nombre de systèmes à hydrogène installés
#n_generateur = ? # nombre de générateurs diesel installés

#Capex pour 1 entité de chaque type
Capex_PV = (float(sheet["G9"].value) if sheet["G9"].value is not None else 0.0) * (float(sheet["G6"].value) if sheet["G6"].value is not None else 0.0)
Capex_WT = (float(sheet["K8"].value) if sheet["K8"].value is not None else 0.0) * (float(sheet["K6"].value) if sheet["K6"].value is not None else 0.0)
Capex_batterie = (float(sheet["C7"].value) if sheet["C7"].value is not None else 0.0) * (float(sheet["C10"].value) if sheet["C10"].value is not None else 0.0)
#Capex_hydro = 
Capex_generateur = (float(sheet["K8"].value) if sheet["K8"].value is not None else 0.0) * (float(sheet["K8"].value) if sheet["K8"].value is not None else 0.0)


#Opex pour 1 entité ; On va les créer sous forme de liste avec chaque élément qui correspondra à une année distincte
Discount_rate = (float(sheet["AA6"].value) if sheet["AA6"].value is not None else 0.0)


Opex_PV = []
opex_annuel_PV = (float(sheet["G8"].value) if sheet["G8"].value is not None else 0.0) * (float(sheet["G6"].value) if sheet["G6"].value is not None else 0.0)

for i in range(25) : 
    opex_annualise_PV = opex_annuel_PV/(1+Discount_rate)**i
    Opex_PV.append(opex_annualise_PV)

#print(Opex_PV)
#print(opex_annuel_PV)
#print(Discount_rate)


Opex_WT = []
opex_annuel_WT = (float(sheet["K9"].value) if sheet["K9"].value is not None else 0.0) * (float(sheet["K6"].value) if sheet["K6"].value is not None else 0.0)
for i in range(25) : 
    opex_annualise_WT = opex_annuel_WT/(1+Discount_rate)**i
    Opex_WT.append(opex_annualise_WT)
#print(Opex_WT)


Opex_batterie = []
opex_annuel_batterie = (float(sheet["C7"].value) if sheet["C7"].value is not None else 0.0) * (float(sheet["C9"].value) if sheet["C9"].value is not None else 0.0)
for i in range(25) : 
    opex_annualise_batterie = opex_annuel_batterie/(1+Discount_rate)**i
    Opex_batterie.append(opex_annualise_batterie)

#print(Opex_batterie)
    

Opex_generateur = []
opex_annuel_generateur = (float(sheet["S9"].value) if sheet["S9"].value is not None else 0.0) * (float(sheet["S6"].value) if sheet["S6"].value is not None else 0.0)
for i in range(25) :
    opex_annualise_generateur = opex_annuel_generateur/(1+Discount_rate)**i
    Opex_generateur.append(opex_annualise_generateur)

print(Opex_generateur)