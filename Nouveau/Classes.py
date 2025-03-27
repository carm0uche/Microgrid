class PV:
    def __init__(self, name, lifetime, power, derating_factor, capex, opex, efficiency):
        """
        """
        self.name = name
        self.lifetime = lifetime
        self.power = power
        self.derating_factor = derating_factor
        self.capex = capex
        self.opex = opex
        self.efficiency = efficiency

    def display_info(self):
        """Affiche les informations sur la source d'énergie."""
        print(f"Nom: {self.name}")
        print(f"Durée de vie: {self.lifetime} années")
        print(f"Puissance: {self.power} kW")
        print(f"Derating factor : {self.derating_factor}")
        print(f"CAPEX: {self.capex} €/kWc/an")
        print(f"OPEX: {self.opex} €/kWc")
        print(f"Rendement STC: {self.efficiency}")

class WT:
    def __init__(self, name, lifetime, rated_power, capex, opex, P_v):
        """
        """
        self.name = name
        self.lifetime = lifetime
        self.rated_power = rated_power
        self.capex = capex
        self.opex = opex
        self.P_v = P_v

    def display_info(self):
        """Affiche les informations sur la source d'énergie."""
        print(f"Nom: {self.name}")
        print(f"Durée de vie: {self.lifetime} années")
        print(f"Puissance nominale: {self.rated_power} kW")
        print(f"CAPEX: {self.capex} €/kW")
        print(f"OPEX: {self.opex} €/kW/an")
        print(f"Puissance en fonction de la vitesse du vent: {self.P_v[:10]},...")

class Fuel:
    def __init__(self, name, lifetime, max_power, capex, opex, salvage, max_use, fuel_cost):
        """
        """
        self.name = name
        self.lifetime = lifetime
        self.max_power = max_power
        self.capex = capex
        self.opex = opex
        self.salvage = salvage
        self.max_use = max_use
        self.fuel_cost = fuel_cost

    def display_info(self):
        """Affiche les informations sur la source d'énergie."""
        print(f"Nom: {self.name}")
        print(f"Durée de vie: {self.lifetime} années")
        print(f"Puissance: {self.max_power} kW")
        print(f"CAPEX: {self.capex} €/kW")
        print(f"OPEX: {self.opex} €/kW/an")
        print(f"Prix de récupération: {self.salvage} €")
        print(f"Prix du carburant: {self.fuel_cost} €")

class Hydrogen:
    def __init__(self, name, lifetime, capacity, efficiency, capex_el, opex_el, capex_tank, opex_tank, capex_fc, opex_fc, salvage, max_start, max_use, charge_pw_max):
        """
        """
        self.name = name
        self.lifetime = lifetime
        self.capacity = capacity
        self.efficiency = efficiency
        self.capex_el = capex_el
        self.opex_el = opex_el
        self.capex_tank = capex_tank
        self.opex_tank = opex_tank
        self.capex_fc = capex_fc
        self.opex_fc = opex_fc
        self.salvage = salvage
        self.max_start = max_start
        self.max_use = max_use
        self.charge_pw_max = charge_pw_max

    def display_info(self):
        """Affiche les informations sur la source d'énergie."""
        print(f"Nom: {self.name}")
        print(f"Durée de vie: {self.lifetime} années")
        print(f"Capacité de stockage: {self.capacity} kWh")
        print(f"Efficacité: {self.efficiency} %")
        print(f"CAPEX électrolyseur: {self.capex_el} €/kW")
        print(f"OPEX électrolyseur: {self.opex_el} €/kW/an")
        print(f"CAPEX H2 tank: {self.capex_tank} €/kg")
        print(f"OPEX H2 tank: {self.opex_tank} €/kg/an")
        print(f"CAPEX fc: {self.capex_fc} €/kW")
        print(f"OPEX fc: {self.opex_fc} €/kW/an")
        print(f"Prix de récupération: {self.salvage} €")
        print(f"Nombre de démarrages max: {self.max_start}")
        print(f"Durée d'utilisation max: {self.max_use} h")

class Batt:
    def __init__(self, name, lifetime, capacity, efficiency, capex, opex, state_charge_min, thrpt, charge_pw_max, discharge_pw_max):
        self.name = name
        self.lifetime = lifetime
        self.capacity = capacity
        self.efficiency = efficiency
        self.capex = capex
        self.opex = opex
        self.state_charge_min = state_charge_min
        self.thrpt = thrpt
        self.charge_pw_max = charge_pw_max
        self.discharge_pw_max =  discharge_pw_max

    def display_info(self):
        """Affiche les informations sur la source d'énergie."""
        print(f"Nom: {self.name}")
        print(f"Durée de vie: {self.lifetime} années")
        print(f"Capacité: {self.capacity} kWh")
        print(f"Efficacité: {self.efficiency}")
        print(f"CAPEX: {self.capex} €/kWh/an")
        print(f"OPEX: {self.opex} €/kWh")
        print(f"État de charge minimal = {self.state_charge_min} kWh")
        print(f"THRPT = {self.thrpt} kWh/kW")
        print(f"Puissance de charge max: = {self.charge_pw_max} kW")
        print(f"Puissance de décharge max: = {self.discharge_pw_max} kW")

    





