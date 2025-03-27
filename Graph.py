import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Calculs_new import *

hours = np.arange(24)
Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage = calcul_simu([2000,1,1,10,10])
Power_WT = np.array(Power_WT)
Power_PV = np.array(Power_PV)
Power_gen = np.array(Power_gen)
level_batt = np.array(level_batt)
level_h2 = np.array(level_h2)
curtailment = np.array(curtailment)
shortage = np.array(shortage)
loadg = np.array(load[:24])


# Création de la figure
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

# Zones empilées de production et stockage
ax.fill_between(hours, 0, Power_WT, label="Éolien", color="cornflowerblue", alpha=0.7)
ax.fill_between(hours, Power_WT, Power_WT + Power_PV, label="Solaire", color="gold", alpha=0.7)
ax.fill_between(hours, Power_WT + Power_PV, Power_WT + Power_PV + Power_gen, label="Générateur", color="darkorange", alpha=0.7)

# Charge en ligne noire
ax.plot(hours, loadg, color="black", linewidth=2, linestyle="dashed", label="Charge")

# Curtailment en gris
ax.fill_between(hours, Power_WT + Power_PV + Power_gen  , 
                Power_WT + Power_PV + Power_gen + curtailment, 
                color="gray", alpha=0.5, label="Surplus (Curtailment)")

# Shortage en rouge sous zéro
ax.fill_between(hours, shortage, 0, color="red", alpha=0.6, label="Pénurie (Shortage)")

# Mise en forme
ax.set_xlabel("Heures")
ax.set_ylabel("Puissance (kW)")
ax.set_title("Évolution de la production et charge sur 24h")
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.xticks(hours)
plt.grid(True, linestyle="--", alpha=0.6)

plt.show()

sns.set_style("whitegrid")
fig, ax1 = plt.subplots(figsize=(12, 6))

# Tracé du niveau de batterie
ax1.plot(hours, level_batt, label="Batterie", color="blue", linewidth=2)
ax1.set_xlabel("Heures")
ax1.set_ylabel("Stockage Batterie (kWh)")
ax1.set_title("Évolution du stockage (batterie et hydrogène) sur 24h")
ax1.legend(loc="upper left", bbox_to_anchor=(1, 1))
ax1.grid(True, linestyle="--", alpha=0.6)

# Création d'un deuxième axe y pour le niveau d'hydrogène
ax2 = ax1.twinx()
ax2.plot(hours, level_h2, label="Hydrogène", color="mediumseagreen", linewidth=2)
ax2.set_ylabel("Stockage Hydrogène (kWh)")

# Affichage des capacités maximales
ax1.axhline(y=Batterie.capacity * 10, color='black', linestyle='--', label='Batterie Capacité Max')
ax2.axhline(y=Stockage_hydrogene.capacity * 10, color='red', linestyle='--', label='Hydrogène Capacité Max')

# Ajout des légendes pour les capacités maximales
ax1.legend(loc="upper left", bbox_to_anchor=(1, 0.9))
ax2.legend(loc="upper left", bbox_to_anchor=(1, 0.85))

plt.xticks(hours)
plt.show()