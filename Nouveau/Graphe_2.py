import numpy as np
from Simu_final import *
import matplotlib.pyplot as plt
import seaborn as sns

def graphique(profile):
    '''
    Graphique sur une année avec un point par semaine (52 points)
    '''
    weeks = np.arange(8760)
    Power_WT, Power_PV, Power_gen, level_batt, level_h2, curtailment, shortage = profile
    
    # Conversion en tableaux numpy
    #Power_WT = np.array(Power_WT[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #Power_PV = np.array(Power_PV[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #Power_gen = np.array(Power_gen[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #level_batt = np.array(level_batt[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #level_h2 = np.array(level_h2[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #curtailment = np.array(curtailment[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #shortage = np.array(shortage[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))
    #loadg = np.array(load[:8736]).reshape(52, 7, 24).mean(axis=(1, 2))

    Power_WT = np.array(Power_WT[:8760])
    Power_PV = np.array(Power_PV[:8760])
    Power_gen = np.array(Power_gen[:8760])
    level_batt = np.array(level_batt[:8760])
    level_h2 = np.array(level_h2[:8760])
    curtailment = np.array(curtailment[:8760])
    shortage = np.array(shortage[:8760])
    loadg = np.array(load[:8760])

    # Création de la figure principale
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))

    # Zones empilées de production et stockage
    ax.fill_between(weeks, 0, Power_WT, label="Éolien", color="cornflowerblue", alpha=0.6)
    ax.fill_between(weeks, Power_WT, Power_WT + Power_PV, label="Solaire", color="gold", alpha=0.6)
    ax.fill_between(weeks, Power_WT + Power_PV, Power_WT + Power_PV + Power_gen, label="Générateur", color="darkorange", alpha=0.6)
    
    # Charge en ligne noire
    ax.plot(weeks, loadg, color="black", linewidth=2, linestyle="dashed", label="Charge")
    
    # Curtailment en gris
    ax.fill_between(weeks, Power_WT + Power_PV + Power_gen, 
                    Power_WT + Power_PV + Power_gen + curtailment, 
                    color="gray", alpha=0.5, label="Surplus (Curtailment)")
    
    # Shortage en rouge sous zéro
    ax.fill_between(weeks, shortage, 0, color="red", alpha=0.6, label="Pénurie (Shortage)")

    # Mise en forme
    ax.set_xlabel("heures")
    ax.set_ylabel("Puissance (kW)")
    ax.set_title("Évolution moyennisée de la production, stockage et charge sur une année")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

    # Graphique des niveaux de batterie
    fig, (ax_batt, ax_h2) = plt.subplots(2,1, figsize=(12, 4), sharex=True)
    ax_batt.plot(weeks, level_batt, color="blue", linewidth=2, label="Niveau de batterie")
    ax_batt.set_xlabel("Semaines")
    ax_batt.set_ylabel("Stockage Batterie (kWh)")
    ax_batt.set_title("Évolution du niveau de batterie sur l'année")
    ax_batt.legend()
    ax_batt.grid(True, linestyle="--", alpha=0.6)
    #plt.show()

    # Graphique des niveaux de stockage hydrogène
    #fig, ax_h2 = plt.subplots(figsize=(12, 4))
    ax_h2.plot(weeks, level_h2, color="green", linewidth=2, label="Stockage H2")
    ax_h2.set_xlabel("Semaines")
    ax_h2.set_ylabel("Stockage H2 (kWh)")
    ax_h2.set_title("Évolution du stockage H2 sur l'année")
    ax_h2.legend()
    ax_h2.grid(True, linestyle="--", alpha=0.6)
    plt.show()

#graphique(simulation([10, 5198, 1, 150, [1983, 1, 1383]])[2])
graphique(simulation([3, 5403, 0, 1, [3024, 294, 185]])[2])