import json
import numpy as np
from pnd import Apathy


class Crime:
    def __init__(self, fs="filespace/"):
        self.l_file = fs+"final.json"
        self.averages = [8, 32]
        self.raw_days = 4
        self.data = {}
        self.days = []
        self.keys = [
            "aa_count",
            "total_aa_score",
            "city_count",
            "total_infrastructure",
            "total_land",
            "oil_pp",
            "wind_pp",
            "coal_pp",
            "nuclear_pp",
            "coal_mines",
            "oil_wells",
            "uranium_mines",
            "iron_mines",
            "lead_mines",
            "bauxite_mines",
            "farms",
            "supermarkets",
            "banks",
            "shopping_malls",
            "stadiums",
            "oil_refineries",
            "aluminum_refineries",
            "steel_mills",
            "munitions_factories",
            "nation_count",
            "total_score",
            "total_population",
            "beige",
            "soldiers",
            "tanks",
            "aircraft",
            "ships",
            "missiles",
            "nukes",
            "gray",
            "blitzkrieg",
            "credits_sell_total_value",
            "credits_buy_total_value",
            "credits_sell_quantity",
            "credits_buy_quantity",
            "food_sell_total_value",
            "food_buy_total_value",
            "food_sell_quantity",
            "food_buy_quantity",
            "coal_sell_total_value",
            "coal_buy_total_value",
            "coal_sell_quantity",
            "coal_buy_quantity",
            "oil_sell_total_value",
            "oil_buy_total_value",
            "oil_sell_quantity",
            "oil_buy_quantity",
            "uranium_sell_total_value",
            "uranium_buy_total_value",
            "uranium_sell_quantity",
            "uranium_buy_quantity",
            "lead_sell_total_value",
            "lead_buy_total_value",
            "lead_sell_quantity",
            "lead_buy_quantity",
            "iron_sell_total_value",
            "iron_buy_total_value",
            "iron_sell_quantity",
            "iron_buy_quantity",
            "bauxite_sell_total_value",
            "bauxite_buy_total_value",
            "bauxite_sell_quantity",
            "bauxite_buy_quantity",
            "gasoline_sell_total_value",
            "gasoline_buy_total_value",
            "gasoline_sell_quantity",
            "gasoline_buy_quantity",
            "munitions_sell_total_value",
            "munitions_buy_total_value",
            "munitions_sell_quantity",
            "munitions_buy_quantity",
            "steel_sell_total_value",
            "steel_buy_total_value",
            "steel_sell_quantity",
            "steel_buy_quantity",
            "aluminum_sell_total_value",
            "aluminum_buy_total_value",
            "aluminum_sell_quantity",
            "aluminum_buy_quantity",
            "credits_sell_average_price",
            "credits_buy_average_price",
            "food_sell_average_price",
            "food_buy_average_price",
            "coal_sell_average_price",
            "coal_buy_average_price",
            "oil_sell_average_price",
            "oil_buy_average_price",
            "uranium_sell_average_price",
            "uranium_buy_average_price",
            "lead_sell_average_price",
            "lead_buy_average_price",
            "iron_sell_average_price",
            "iron_buy_average_price",
            "bauxite_sell_average_price",
            "bauxite_buy_average_price",
            "gasoline_sell_average_price",
            "gasoline_buy_average_price",
            "munitions_sell_average_price",
            "munitions_buy_average_price",
            "steel_sell_average_price",
            "steel_buy_average_price",
            "aluminum_sell_average_price",
            "aluminum_buy_average_price",
            "infra_destroyed",
            "aircraft_destroyed",
            "missiles_used",
            "nukes_used",
            "raid_count",
            "attrition_count",
            "ordinary_count"
        ]

    def load(self):
        with open(self.l_file) as f:
            self.data = json.load(f)

    def process(self, day):
        if day < self.raw_days:
            return None
        out = self.days[day:day-self.raw_days-1:-1].copy()
        for i in range(len(self.averages)):
            if day < self.averages[i]:
                return None
            out += [np.average(self.days[day-self.averages[i]:day], axis=0)]
        return np.array(out)

    def organize(self):
        if not len(self.data):
            self.load()
        keys = [float(k) for k in self.data.keys()]
        keys.sort()
        self.days = [np.array([self.data[str(k)][key] for key in self.keys]) for k in keys]

        out = []
        for i in range(len(self.days)):
            processed = self.process(i)
            if processed is None:
                continue
            else:
                out.append(processed)
        return out

    def full_run(self, apathy=Apathy):
        apathy().run()
        return self.organize()
