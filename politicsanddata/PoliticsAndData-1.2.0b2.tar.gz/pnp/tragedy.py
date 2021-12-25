"""
Contains :py:class:`Tragedy`.
"""

import random
import pickle
import numpy as np

rand = np.random.default_rng()
np.seterr(all="raise")

relu = lambda x: x * (x > 0)
relu_deriv = lambda x: x > 0
get_delta = lambda e, w: e.dot(w.T)
get_weight_update = lambda l, d: l.T.dot(d)


class Tragedy:
    """ """

    def __init__(self, loc="filespace/"):
        self.file = f"{loc}weights.pkl"
        self.output_labels = [
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
        self.data_length = 115
        self.day_widths = [
            self.data_length,
            96,
            64,
            48
        ]
        self.widths = [
            self.day_widths[-1] * 6,  # 4 days raw, 8-day average, 32-day average
            256,
            128,
            len(self.output_labels)
        ]
        self.batch_size = 32
        self.dataset = []
        self.training_data = {}
        self.alpha = 0.0001

        try:
            self.load()
        except IOError:
            if input("Initialize weights? (y/n) ") == "y" and \
                    input(f"Are you sure? {self.file} will be written over. (y/n) "):
                self.init_weights(True)
            else:
                print("Cancelled.")

    def load(self):
        """ """
        with open(self.file, "rb") as f:
            data = pickle.load(f)
            self.weights = data["weights"]
            self.day_weights = data["day_weights"]

    def save(self):
        """ """
        with open(self.file, "wb") as f:
            pickle.dump({
                "weights": self.weights,
                "day_weights": self.day_weights
            }, f, pickle.HIGHEST_PROTOCOL)

    def add_dataset(self, ds: list):
        for data in ds:
            if not isinstance(data, np.ndarray):
                raise TypeError("Data is not a numpy array.")
            for group in data:
                if len(group) != self.day_widths[0]:
                    raise ValueError("Data width does not match neural network width.")
        self.dataset += ds

    def init_weights(self, confirm=False):
        """
        :param confirm:  (Default value = False)
        """
        if confirm:
            self.weights = [
                rand.normal(
                    size=(self.widths[i], self.widths[i + 1]),
                    loc=0,
                    scale=(2 / (self.widths[i] + self.widths[i + 1])) ** (1 / 2)
                ) for i in range(len(self.widths) - 1)
            ]
            self.day_weights = [
                rand.normal(
                    size=(self.day_widths[i], self.day_widths[i + 1]),
                    loc=0,
                    scale=(2 / (self.day_widths[i] + self.day_widths[i + 1])) ** (1 / 2)
                ) for i in range(len(self.day_widths) - 1)
            ]
            self.save()

    def predict(self, inp, dropout=False):
        layer0 = []
        for group in inp:
            layer0.append(self.forward_prop(
                group,
                self.day_widths,
                self.day_weights,
                note="day"
            ))
        if dropout:
            mask = [
                rand.integers(2, size=width) * 2 for width in self.widths[:-1:]
            ]
        else:
            mask = None
        layers = self.forward_prop(
            np.concatenate([group[-1] for group in layer0]),
            self.widths,
            self.weights,
            mask
        )
        self.training_data = {
            "day_layers": layer0,
            "layers": layers
        }
        return layers[-1]

    def train(self, data=None):
        day_weight_updates = [
            np.zeros(shape=w.shape) for w in self.day_weights
        ]
        weight_updates = [
            np.zeros(shape=w.shape) for w in self.weights
        ]
        total_error = 0
        for i in range(self.batch_size):
            if data is None or i >= len(data):
                inp = random.choice(self.dataset)
            else:
                inp = data[i]
            updates = self.find_weight_update(inp)
            for j in range(len(day_weight_updates)):
                day_weight_updates[j] += updates[0][j]
            for j in range(len(weight_updates)):
                weight_updates[j] += updates[1][j]
            total_error += updates[2].sum()
        for i in range(len(self.day_weights)):
            self.day_weights[i] += day_weight_updates[i]
        for i in range(len(self.weights)):
            self.weights[i] += weight_updates[i]

        self.save()
        return total_error/self.batch_size

    def find_weight_update(self, data):
        expected = data[0]
        pred = self.predict(data[1:], dropout=True)
        day_layers = self.training_data["day_layers"]
        layers = self.training_data["layers"]

        delta = expected-pred
        error = delta ** 2

        real_updates = []
        for i in range(len(layers) - 1, 0, -1):
            real_updates.append(get_weight_update(layers[i], delta)*self.alpha)
            delta = get_delta(delta, self.weights[i-1]) * relu_deriv(layers[i-1])
        day_updates = [
            np.zeros(shape=weight.shape) for weight in self.day_weights
        ]
        for delta in np.split(delta, 6):
            for i in range(len(layers) - 2, -1):
                day_updates.append(get_weight_update(day_layers[i], delta)*self.alpha)
                delta = get_delta(delta, self.day_weights[i]) * relu_deriv(day_layers[i])

        return day_updates, real_updates, error  # weight update + error (day, real, error)

    def find_error(self, data):
        return np.sum((data[0] - self.predict(data[1:])) ** 2)

    def forward_prop(self, layer0, widths, weights, mask=None, note=""):
        """ """
        layers = [layer0] + [
            np.array([0.0] * width) for width in widths[1::]
        ]
        for i in range(len(layers) - 1):
            if mask is not None:
                try:
                    layers[i] *= mask[i]
                except FloatingPointError:
                    print("Error values exist.", note)
                    print("layer", i, layers[i])
                    print("weights", i, weights[i])
                    exit()
            layers[i + 1] = layers[i].dot(weights[i])
            if i != len(layers)-1:
                layers[i+1] = relu(layers[i+1])
        return layers
