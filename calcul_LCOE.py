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

Capex_PV = float(sheet["G9"].value) if sheet["G9"].value is not None else 0.0       #en $/kWc ; à clarifier 
Capex_WT = (float(sheet["K8"].value) if sheet["K8"].value is not None else 0.0) * ((float(sheet["K6"].value) if sheet["K6"].value is not None else 0.0))

print(Capex_PV)
