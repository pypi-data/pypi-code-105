import numpy as np


class EnsembleControls:

    def __init__(self, settings):
        self.settings = settings

    def get_nt_for_ge_1(self, ge):
        return self.settings["key_rank_attack_traces"] - np.argmax(ge[::-1] > 2) * self.settings["key_rank_report_interval"]

    def get_nt_for_sr_thre(self, sr, thre):
        return self.settings["key_rank_attack_traces"] - np.argmax(sr[::-1] < thre) * self.settings["key_rank_report_interval"]

    def order_models_per_guessing_entropy(self, ge_values, number_of_models):

        """ Order models by the number of validation traces required to achieve GE = 1"""

        result_number_of_traces_ge_1 = []
        for model_index, ge in enumerate(ge_values):
            nt_ge_1 = self.get_nt_for_ge_1(ge) if ge[len(ge) - 1] < 2 else self.settings["key_rank_attack_traces"]
            result_number_of_traces_ge_1.append([ge[len(ge) - 1], nt_ge_1, model_index])

        sorted_models = sorted(result_number_of_traces_ge_1, key=lambda l: l[:])

        list_of_best_models = []
        for model_index in range(number_of_models):
            list_of_best_models.append(sorted_models[model_index][2])

        return list_of_best_models

    def order_models_per_success_rate(self, sr_values, thre, number_of_best_models):

        result_number_of_traces_sr_1 = []
        for model_index, sr in enumerate(sr_values):
            nt_sr_1 = self.get_nt_for_sr_thre(sr, thre) if sr[len(sr) - 1] > thre else self.settings["key_rank_attack_traces"]
            result_number_of_traces_sr_1.append([sr[len(sr) - 1], nt_sr_1, model_index])

        sorted_models = sorted(result_number_of_traces_sr_1, key=lambda l: l[:])

        list_of_best_models = []
        for model_index in range(number_of_best_models):
            list_of_best_models.append(sorted_models[model_index][2])

        return list_of_best_models
