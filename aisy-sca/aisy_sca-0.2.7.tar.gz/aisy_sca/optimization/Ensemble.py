from aisy_sca.optimization.EnsembleControls import EnsembleControls
from aisy_sca.AnalysisDatabaseControls import AnalysisDatabaseControls
from sklearn.utils import shuffle
import numpy as np
import random


class Ensemble:

    def __init__(self, settings, dataset):
        self.settings = settings
        self.dataset = dataset

    def compute(self, sk_all_models, number_of_best_models, labels_key_hypothesis_attack, db_controls, early_stopping_metric=None,
                n_profiling=None):

        ens_controls = EnsembleControls(self.settings)
        if early_stopping_metric is not None:
            ge_all_validation, ge_all_attack = db_controls.select_all_early_stopping_guessing_entropy_from_analysis(early_stopping_metric,
                                                                                                                    n_profiling=n_profiling)
            # sr_all_validation, sr_all_attack = db_controls.select_all_early_stopping_success_rate_from_analysis(early_stopping_metric,
            #                                                                                                     n_profiling=n_profiling)
        else:
            ge_all_validation, ge_all_attack = db_controls.select_all_guessing_entropy_from_analysis(n_profiling=n_profiling)
            # sr_all_validation, sr_all_attack = db_controls.select_all_success_rate_from_analysis(n_profiling=n_profiling)

        number_of_models = len(ge_all_validation)

        nt_interval = int(self.settings["key_rank_attack_traces"] / self.settings["key_rank_report_interval"])

        list_of_best_models = ens_controls.order_models_per_guessing_entropy(ge_all_validation, number_of_models)

        # ge_best_model_validation = ge_all_validation[list_of_best_models[0]]
        # ge_best_model_attack = ge_all_attack[list_of_best_models[0]]
        # sr_best_model_validation = sr_all_validation[list_of_best_models[0]]
        # sr_best_model_attack = sr_all_attack[list_of_best_models[0]]

        kr_ensemble = np.zeros(nt_interval)
        krs_ensemble = np.zeros((self.settings["key_rank_executions"], nt_interval))
        kr_ensemble_best_models = np.zeros(nt_interval)
        krs_ensemble_best_models = np.zeros((self.settings["key_rank_executions"], nt_interval))

        nt = len(self.dataset.x_attack)

        probabilities_kg_all_traces = np.zeros((number_of_models, nt, 256))

        for model_index in range(number_of_models):

            out_prob_model = sk_all_models[list_of_best_models[model_index]]
            for index in range(self.settings["key_rank_attack_traces"]):
                probabilities_kg_all_traces[model_index][index] = out_prob_model[index][
                    np.asarray([int(leakage[index]) for leakage in labels_key_hypothesis_attack[:]])
                ]
            print(f"Processing Model {list_of_best_models[model_index]} of {number_of_models}")

        random_states_ensembles = []

        for run in range(self.settings["key_rank_executions"]):

            key_p_ensemble = np.zeros(256)
            key_p_ensemble_best_models = np.zeros(256)

            probabilities_kg_all_traces_shuffled = np.zeros((number_of_models, nt, 256))
            # if self.settings["reproducible"]:
            #     random_state = self.ge_sr_random_states_ensemble[run]
            # else:
            #     random_state = random.randint(0, 100000)
            random_state = random.randint(0, 100000)
            random_states_ensembles.append(random_state)
            for model_index in range(number_of_models):
                probabilities_kg_all_traces_shuffled[model_index] = shuffle(probabilities_kg_all_traces[model_index],
                                                                            random_state=random_state)

            kr_count = 0
            for index in range(self.settings["key_rank_attack_traces"]):
                for model_index in range(number_of_models):
                    key_p_ensemble += np.log(probabilities_kg_all_traces_shuffled[model_index][index] + 1e-36)
                for model_index in range(number_of_best_models):
                    key_p_ensemble_best_models += np.log(probabilities_kg_all_traces_shuffled[model_index][index] + 1e-36)

                key_p_ensemble_sorted = np.argsort(key_p_ensemble)[::-1]
                key_p_ensemble_best_models_sorted = np.argsort(key_p_ensemble_best_models)[::-1]

                if (index + 1) % self.settings["key_rank_report_interval"] == 0:
                    kr_position = list(key_p_ensemble_sorted).index(self.settings["good_key"]) + 1
                    kr_ensemble[kr_count] += kr_position
                    krs_ensemble[run][kr_count] = kr_position

                    kr_position = list(key_p_ensemble_best_models_sorted).index(self.settings["good_key"]) + 1
                    kr_ensemble_best_models[kr_count] += kr_position
                    krs_ensemble_best_models[run][kr_count] = kr_position
                    kr_count += 1

            print("Run: {} | GE {} models: {} | GE {} best models: {}".format(run, number_of_models,
                                                                              kr_ensemble[nt_interval - 1] / (run + 1),
                                                                              number_of_best_models,
                                                                              kr_ensemble_best_models[nt_interval - 1] / (run + 1)))

        self.settings["ge_sr_random_states_ensemble"] = random_states_ensembles

        ge_ensemble = kr_ensemble / self.settings["key_rank_executions"]
        ge_ensemble_best_models = kr_ensemble_best_models / self.settings["key_rank_executions"]

        sr_ensemble = np.zeros(nt_interval)
        sr_ensemble_best_models = np.zeros(nt_interval)

        for index in range(nt_interval):
            for run in range(self.settings["key_rank_executions"]):
                sr_ensemble[index] += 1 if krs_ensemble[run][index] == 1 else 0
                sr_ensemble_best_models[index] += 1 if krs_ensemble_best_models[run][index] == 1 else 0

        sr_ensemble = sr_ensemble / self.settings["key_rank_executions"]
        sr_ensemble_best_models = sr_ensemble_best_models / self.settings["key_rank_executions"]

        if early_stopping_metric is not None:
            if n_profiling is not None:
                label_ensemble = f"Ensemble {early_stopping_metric} {n_profiling} traces"
            else:
                label_ensemble = f"Ensemble {early_stopping_metric}"
        else:
            if n_profiling is not None:
                label_ensemble = f"Ensemble {n_profiling} traces"
            else:
                label_ensemble = "Ensemble"

        """ save guessing entropy from ensemble calculation to database"""
        db_controls.save_ensemble_guessing_entropy_results(ge_ensemble, label_ensemble)
        db_controls.save_ensemble_guessing_entropy_results(ge_ensemble_best_models,
                                                           f"{label_ensemble} of Best {number_of_best_models} Models")

        """ save success_rate from ensemble calculation to database"""
        db_controls.save_ensemble_success_rate_results(sr_ensemble, label_ensemble)
        db_controls.save_ensemble_success_rate_results(sr_ensemble_best_models, f"{label_ensemble} of Best {number_of_best_models} Models")
