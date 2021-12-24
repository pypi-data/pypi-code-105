from aisy_sca.optimization.HyperparameterSearch import *
from aisy_sca.sca.Profiling import Profiling
from aisy_sca.utils import Utils
import tensorflow.keras.backend as backend
from termcolor import colored
import itertools
import json
import time


class RandomGridSearch(HyperparameterSearch):
    """
    Class that perform random or grid hyper-parameter search .
    The random search only supports MLPs and CNNs.
    """

    def __init__(self, settings, dataset, random_search_definitions, labels_key_guesses_attack_set, labels_key_guesses_validation_set,
                 analysis_db_controls, random_states=None):
        super().__init__(settings, dataset, random_search_definitions, labels_key_guesses_attack_set, labels_key_guesses_validation_set,
                         analysis_db_controls, random_states=None)
        self.custom_callbacks = {}

    def run(self, hp_combinations_reproducible, da_function=None, grid_search=False):

        hp_search_ranges = self.random_search_definitions["hyper_parameters_search"]
        hp_ids = []
        model_descriptions = []
        if self.random_states is None:
            if grid_search:
                hp_to_search = {}
                hp_to_adjust = {}
                for hp, hp_value in hp_search_ranges.items():
                    if type(hp_value) is str:
                        hp_to_adjust[hp] = hp_value
                    else:
                        hp_to_search[hp] = hp_value
                keys, value = zip(*hp_to_search.items())
                search_hp_combinations = [dict(zip(keys, v)) for v in itertools.product(*value)]
                for idx in range(len(search_hp_combinations)):
                    for hp, hp_value in hp_to_adjust.items():
                        search_hp_combinations[idx][hp] = hp_value

                self.random_search_definitions["max_trials"] = len(search_hp_combinations)
                print("======================================================================================")
                print(f"Number of hyperparameters combinations for grid search: {len(search_hp_combinations)}")
                print("======================================================================================")
            else:
                search_hp_combinations = hp_search_ranges
        else:
            search_hp_combinations = hp_combinations_reproducible

        start = time.time()

        for search_index in range(self.random_search_definitions["max_trials"]):

            """ Generate a random/grid CNN or MLP model """
            if self.random_states is None:
                hp_values = search_hp_combinations[search_index] if grid_search else search_hp_combinations
            else:
                hp_values = search_hp_combinations[search_index]
            model, hp = self.generate_model(hp_values)

            print(colored(f"Hyper-Parameters for Search {search_index}: {json.dumps(hp, sort_keys=True, indent=4)}", "blue"))

            model_descriptions.append(Utils().keras_model_as_string(model, f"best_model_{search_index}"))

            """ Run profiling/training phase """
            profiling = Profiling(self.settings, self.dataset, da_function)
            history = profiling.train_model(model)
            self.custom_callbacks[f"{search_index}"] = profiling.get_custom_callbacks()

            """ Save hyperparameters combination to database and receive the id of the insertion (hp_id)"""
            hyper_parameters_list = self.set_hyper_parameters_list(hp, model)
            hp_id = self.analysis_db_controls.save_hyper_parameters_to_database(hyper_parameters_list)
            hp_ids.append(hp_id)

            """ Retrieve metrics from model and save them to database """
            self.loss_search.append(history.history["loss"])
            self.acc_search.append(history.history["accuracy"])

            """ Compute SCA metrics and save them to database """
            self.compute_metrics(model, search_index, self.analysis_db_controls, profiling.get_builtin_callbacks(), hp_id)
            ge = self.ge_search[search_index]
            sr = self.sr_search[search_index]
            hyper_parameters_list = self.update_hyper_parameters_list(hp, ge, sr)
            self.analysis_db_controls.update_hyper_parameters_to_database(hyper_parameters_list, hp_id)

            """ Save generic metrics (loss, accuracy, early stopping metrics) to database """
            self.save_generic_metrics(profiling, history, search_index, hp_id)

            """ Update results in database """
            self.analysis_db_controls.update_results_in_database(time.time() - start)

            backend.clear_session()

            """ Find best model"""
            self.get_best_model()

            """ Save best model so far in h5 """
            self.save_best_model(model, search_index)

            """ Check if stopping condition is satisfied"""
            if self.check_stop_condition(search_index, hp):
                self.finalize_search(profiling, model_descriptions, hp_ids)
                break

            if search_index == self.random_search_definitions["max_trials"] - 1:
                self.finalize_search(profiling, model_descriptions, hp_ids)

        """ update database settings"""
        self.analysis_db_controls.update_results_in_database(time.time() - start)

    def get_custom_callbacks(self):
        return self.custom_callbacks
