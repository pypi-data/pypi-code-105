from aisy_sca.optimization.KerasCNNRandom import KerasCNNRandom
from aisy_sca.optimization.KerasMLPRandom import KerasMLPRandom
from aisy_sca.optimization.KerasCNNGrid import KerasCNNGrid
from aisy_sca.optimization.KerasMLPGrid import KerasMLPGrid
from aisy_sca.metrics.SCAMetrics import *
from termcolor import colored
import numpy as np
import os
import json
import random


class HyperparameterSearch:

    def __init__(self, settings, dataset, random_search_definitions, labels_key_guesses_attack_set, labels_key_guesses_validation_set,
                 analysis_db_controls, random_states=None):
        self.settings = settings

        """ set dataset structure: 
                - profiling, validation and attack traces
                - profiling, validation and attack labels
                - profiling, validation and attack plaintexts
                - profiling, validation and attack ciphertexts
                - profiling, validation and attack keys
                """
        self.dataset = dataset

        """ random search definitions """
        self.random_search_definitions = random_search_definitions
        self.analysis_db_controls = analysis_db_controls

        """ Labels for key guesses """
        self.labels_key_guesses_attack_set = labels_key_guesses_attack_set
        self.labels_key_guesses_validation_set = labels_key_guesses_validation_set

        """ Metrics """
        self.sk_attack = []
        self.sk_attack_pa = {}
        self.sk_attack_es = {}
        self.ge_search = []
        self.sr_search = []
        self.loss_search = []
        self.acc_search = []
        self.ge_search_pa = {}
        self.sr_search_pa = {}
        self.loss_search_pa = {}
        self.acc_search_pa = {}
        self.ge_search_early_stopping = {}
        self.sr_search_early_stopping = {}
        self.best_model_index = 0
        self.best_model_index_pa = {}

        """ List of searched hyper-parameters combinations """
        self.hp_searches = []

        """ custom loss """
        self.loss_function = None

        self.random_states = random_states

    def set_metrics(self):

        if self.settings["profiling_analyzer_steps"] is not None:
            for n_profiling_traces in self.settings["profiling_analyzer_steps"]:
                self.ge_search_pa[f"{n_profiling_traces}"] = []
                self.sr_search_pa[f"{n_profiling_traces}"] = []
                self.loss_search_pa[f"{n_profiling_traces}"] = []
                self.acc_search_pa[f"{n_profiling_traces}"] = []
                self.best_model_index_pa[f"{n_profiling_traces}"] = 0
                self.sk_attack_pa[f"{n_profiling_traces}"] = []

    def get_sk_attack(self):
        return self.sk_attack

    def get_sk_attack_pa(self):
        return self.sk_attack_pa

    def get_sk_attack_es(self):
        return self.sk_attack_es

    def update_epochs_and_batch_size(self, hp, hyperparameters):

        hp_values = self.random_search_definitions["hyper_parameters_search"]

        """ check if user requested search for epochs """
        if "epochs" in hp_values:
            self.settings["epochs"] = hyperparameters["epochs"] if self.random_states is not None else random.randrange(
                hp_values["epochs"]["min"],
                hp_values["epochs"]["max"] + hp_values["epochs"]["step"],
                hp_values["epochs"]["step"])
        hp["epochs"] = self.settings["epochs"]

        """ check if user requested search for batch-size """
        if "batch_size" in hp_values:
            self.settings["batch_size"] = hyperparameters["batch_size"] if self.random_states is not None else random.randrange(
                hp_values["batch_size"]["min"],
                hp_values["batch_size"]["max"] +
                hp_values["batch_size"]["step"],
                hp_values["batch_size"]["step"])
        hp["batch_size"] = self.settings["batch_size"]

    def load_model(self, model, setting, idx=None):

        """ Load weights from saved early stopping model from 'resource/models' directory"""

        if idx is None:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}.h5"
        else:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}_{idx}.h5"
        model.load_weights(model_name)

    def delete_model(self, setting, idx=None):

        """ Load model from 'resource/models' directory """

        if idx is None:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}.h5"
        else:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}_{idx}.h5"
        os.remove(model_name)

    def get_early_stopping_metrics(self, early_stopping_metric_results):
        early_stopping_metric_names = []
        for early_stopping_metric in self.settings["early_stopping"]["metrics"]:
            if isinstance(early_stopping_metric_results[early_stopping_metric][0], list):
                for idx in range(len(early_stopping_metric_results[early_stopping_metric][0])):
                    early_stopping_metric_names.append(f"{early_stopping_metric}_{idx}")
            else:
                early_stopping_metric_names.append(early_stopping_metric)
        return early_stopping_metric_names

    def get_early_stopping_values_epochs(self, early_stopping_metric_results):
        early_stopping_values_epochs = {}
        for early_stopping_metric in self.settings["early_stopping"]["metrics"]:
            if isinstance(early_stopping_metric_results[early_stopping_metric][0], list):
                for idx in range(len(early_stopping_metric_results[early_stopping_metric][0])):
                    early_stopping_values_epochs[f"{early_stopping_metric}_{idx}"] = np.array(
                        early_stopping_metric_results[early_stopping_metric])[:, idx]
            else:
                early_stopping_values_epochs[f"{early_stopping_metric}"] = early_stopping_metric_results[early_stopping_metric]
        return early_stopping_values_epochs

    def generate_random_model(self, hp_values):

        """ Generate a random model from hyper-parameters ranges or recreate the model from reproducible settings"""

        if self.random_search_definitions["neural_network"] == "cnn":
            model, hp = KerasCNNRandom(self.settings, hp_values, fixed_model=False if self.random_states is None else True,
                                       loss_function=self.loss_function).cnn_random_search()
        else:
            model, hp = KerasMLPRandom(self.settings, hp_values, fixed_model=False if self.random_states is None else True,
                                       loss_function=self.loss_function).mlp_random_search()
        self.update_epochs_and_batch_size(hp, hp_values)
        return model, hp

    def generate_grid_model(self, hp_values):

        """ Generate a random model from hyper-parameters ranges or recreate the model from reproducible settings"""

        if self.random_search_definitions["neural_network"] == "cnn":
            model, hp = KerasCNNGrid(self.settings, hp_values, fixed_model=False if self.random_states is None else True,
                                     loss_function=self.loss_function).cnn_grid_search()
        else:
            model, hp = KerasMLPGrid(self.settings, hp_values, fixed_model=False if self.random_states is None else True,
                                     loss_function=self.loss_function).mlp_grid_search()
        self.update_epochs_and_batch_size(hp, hp_values)
        return model, hp

    def set_hyper_parameters_list(self, hp, model):
        hyper_parameters_list = {
            "parameters": model.count_params()
        }
        for key, value in hp.items():
            hyper_parameters_list[key] = value
        return hyper_parameters_list

    def update_hyper_parameters_list(self, hp, ge, sr):
        hp["Val GE"] = ge
        hp["Val SR"] = sr
        return hp

    def check_stop_condition(self, search_index, hp):

        """ Check if stopping condition is satisfied """

        search_metric = self.random_search_definitions["metric"]
        stop_value = self.random_search_definitions["stop_value"]
        if self.random_search_definitions["stop_condition"]:
            if search_metric == "guessing_entropy" and self.ge_search[search_index] <= stop_value:
                self.best_model_index = search_index
            elif search_metric == "success_rate" and self.sr_search[search_index] >= stop_value:
                self.best_model_index = search_index
            elif search_metric == "loss" and self.loss_search[search_index] <= stop_value:
                self.best_model_index = search_index
            elif search_metric == "accuracy" and self.acc_search[search_index] >= stop_value:
                self.best_model_index = search_index
            if self.best_model_index == search_index:
                print(colored(f"\nBest Model: {json.dumps(hp, sort_keys=True, indent=4)}", "green"))
                return True
            return False
        return False

    def get_best_model(self, n_profiling_traces=None):

        """ Get search index of best model so far """

        search_metric = self.random_search_definitions["metric"]

        if n_profiling_traces is None:
            if search_metric == "guessing_entropy":
                self.best_model_index = np.argmin(self.ge_search)
            elif search_metric == "success_rate":
                self.best_model_index = np.argmax(self.sr_search)
            elif search_metric == "loss":
                self.best_model_index = np.argmin(self.loss_search)
            elif search_metric == "accuracy":
                self.best_model_index = np.argmax(self.acc_search)
            else:
                self.best_model_index = np.argmin(self.ge_search)

            return self.best_model_index
        else:
            if search_metric == "guessing_entropy":
                self.best_model_index_pa[f"{n_profiling_traces}"] = int(np.argmin(self.ge_search_pa[f"{n_profiling_traces}"]))
            elif search_metric == "success_rate":
                self.best_model_index_pa[f"{n_profiling_traces}"] = int(np.argmax(self.sr_search_pa[f"{n_profiling_traces}"]))
            elif search_metric == "loss":
                self.best_model_index_pa[f"{n_profiling_traces}"] = int(np.argmin(self.loss_search_pa[f"{n_profiling_traces}"]))
            elif search_metric == "accuracy":
                self.best_model_index_pa[f"{n_profiling_traces}"] = int(np.argmax(self.acc_search_pa[f"{n_profiling_traces}"]))
            else:
                self.best_model_index_pa[f"{n_profiling_traces}"] = int(np.argmin(self.ge_search_pa[f"{n_profiling_traces}"]))

            return self.best_model_index_pa

    def display_best_model(self):

        """  Display best model so far """
        if self.settings["use_profiling_analyzer"]:
            for step in self.settings["profiling_analyzer_steps"]:
                self.get_best_model(step)

                print("=========================================")
                print(f" Best Model for {step} profiling traces ")
                print("=========================================")
                print(
                    colored(
                        "\nBest Model: {}".format(
                            json.dumps(self.hp_searches[self.best_model_index_pa[f"{step}"]], sort_keys=True, indent=4)),
                        "green"))
        else:
            self.get_best_model()
            print(
                colored("\nBest Model: {}".format(json.dumps(self.hp_searches[self.best_model_index], sort_keys=True, indent=4)), "green"))

    def save_best_model(self, model, search_index, n_profiling_traces=None):

        """ Save best model so far in h5 """

        if self.best_model_index == search_index or search_index == 0:
            search_metric = self.random_search_definitions["metric"]
            folder = self.settings["resources_root_folder"]
            analysis_id = self.settings["analysis_id"]
            if n_profiling_traces is None:
                model.save_weights(f"{folder}models/best_model_random_search_{search_metric}_{analysis_id}.h5")
            else:
                model.save_weights(
                    f"{folder}models/best_model_random_search_{search_metric}_{n_profiling_traces}traces_id_{analysis_id}.h5")

    def update_sk(self, sk, n_profiling_traces):
        if self.settings["use_ensemble"]:
            if self.settings["use_profiling_analyzer"]:
                self.sk_attack_pa[f"{n_profiling_traces}"].append(sk)
            else:
                self.sk_attack.append(sk)

    def update_sk_es(self, sk, es_metric, n_profiling_traces):
        if self.settings["use_ensemble"]:
            if self.settings["use_profiling_analyzer"]:
                self.sk_attack_es[f"{es_metric}"][f"{n_profiling_traces}"].append(sk)
            else:
                if self.settings["use_ensemble"]:
                    self.sk_attack_es[f"{es_metric}"].append(sk)

    def update_ge_and_sr(self, ge, sr, n_profiling_traces):
        if self.settings["use_profiling_analyzer"]:
            self.ge_search_pa[f"{n_profiling_traces}"].append(ge[-1])
            self.sr_search_pa[f"{n_profiling_traces}"].append(sr[-1])
        else:
            self.ge_search.append(ge[-1])
            self.sr_search.append(sr[-1])

    def initialize_early_stopping_ge_and_sr(self, es_metric, steps):
        if self.settings["use_profiling_analyzer"]:
            if len(self.ge_search_early_stopping) == 0:
                self.ge_search_early_stopping[f"{es_metric}"] = {}
                self.sr_search_early_stopping[f"{es_metric}"] = {}
                self.sk_attack_es[f"{es_metric}"] = {}
                for n in steps:
                    self.ge_search_early_stopping[f"{es_metric}"][f"{n}"] = []
                    self.sr_search_early_stopping[f"{es_metric}"][f"{n}"] = []
                    self.sk_attack_es[f"{es_metric}"][f"{n}"] = []
        else:
            if len(self.ge_search_early_stopping) == 0:
                self.ge_search_early_stopping[f"{es_metric}"] = []
                self.sr_search_early_stopping[f"{es_metric}"] = []
                self.sk_attack_es[f"{es_metric}"] = []

    def update_early_stopping_ge_and_sr(self, es_metric, ge, sr, n_profiling_traces):
        if self.settings["use_profiling_analyzer"]:
            self.ge_search_early_stopping[f"{es_metric}"][f"{n_profiling_traces}"].append(ge[-1])
            self.sr_search_early_stopping[f"{es_metric}"][f"{n_profiling_traces}"].append(sr[-1])
        else:
            self.ge_search_early_stopping[f"{es_metric}"].append(ge[-1])
            self.sr_search_early_stopping[f"{es_metric}"].append(sr[-1])

    def save_generic_metrics(self, profiling, history, search_index, hp_id, n_profiling_traces=None):
        if self.settings["use_early_stopping"]:
            early_stopping_metrics = self.get_early_stopping_metrics(
                profiling.get_builtin_callbacks()["early_stopping_callback"].get_metric_results())
            early_stopping_epoch_values = self.get_early_stopping_values_epochs(
                profiling.get_builtin_callbacks()["early_stopping_callback"].get_metric_results())
        else:
            early_stopping_metrics = None
            early_stopping_epoch_values = None
        self.analysis_db_controls.save_generic_metrics(history, early_stopping_metrics, early_stopping_epoch_values, hp_id,
                                                       search_index=search_index, n_profiling_traces=n_profiling_traces)

    def compute_metrics(self, model, search_index, rs_db_controls, builtin_callback, hp_id, n_profiling_traces=None, steps=None,
                        random_states=None):

        """ Compute SCA metrics: guessing entropy and success rate for attack and validation sets """

        """ 
        Compute Guessing Entropy, Success Rate and Number of Traces for Success (GE < 2) for attack and validation sets 
        Return scores/probabilities for each trace (p(l=leakage|trace=x))
        Retrieve random states for reproducibility
        Save results to database
        """

        label_name = f"Attack Set {search_index} {n_profiling_traces} traces" if self.settings[
            "use_profiling_analyzer"] else f"Attack Set {search_index}"
        random_states_ge_sr = random_states[f"{search_index}"][f"{label_name}"] if random_states is not None else None
        ge, sr, nt, sk, r = SCAMetrics(model, self.dataset.x_attack, self.settings, self.labels_key_guesses_attack_set).run(
            random_states=random_states_ge_sr)
        self.update_sk(sk, n_profiling_traces=n_profiling_traces)
        rs_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, search_index)

        label_name = f"Validation Set {search_index} {n_profiling_traces} traces" if self.settings[
            "use_profiling_analyzer"] else f"Validation Set {search_index}"
        random_states_ge_sr = random_states[f"{search_index}"][f"{label_name}"] if random_states is not None else None
        ge, sr, nt, sk, r = SCAMetrics(model, self.dataset.x_validation, self.settings, self.labels_key_guesses_validation_set).run(
            random_states=random_states_ge_sr)
        self.update_ge_and_sr(ge, sr, n_profiling_traces=n_profiling_traces)
        rs_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, search_index)

        """
        For Early Stopping Metrics:
        Compute Guessing Entropy, Success Rate and Number of Traces for Success (GE < 2) for attack and validation sets 
        Return scores/probabilities for each trace (p(l=leakage|trace=x))
        Retrieve random states for reproducibility        
        """

        """ TODO: search for saved h5 models in folder and then run metrics"""

        if self.settings["use_early_stopping"]:

            early_stopping_metrics = self.get_early_stopping_metrics(
                builtin_callback["early_stopping_callback"].get_metric_results())

            for es_metric in early_stopping_metrics:
                """ initialize list """
                self.initialize_early_stopping_ge_and_sr(es_metric, steps)

                self.load_model(model, es_metric)

                print(colored("Computing Guessing Entropy and Success Rate for Attack Set", "green"))
                label_name = f"ES Attack Set {es_metric} {search_index} {n_profiling_traces} traces" if self.settings[
                    "use_profiling_analyzer"] else f"ES Attack Set {es_metric} {search_index}"
                random_states_ge_sr = random_states[f"{search_index}"][f"{label_name}"] if random_states is not None else None
                ge, sr, nt, sk, r = SCAMetrics(model, self.dataset.x_attack, self.settings, self.labels_key_guesses_attack_set).run(
                    random_states=random_states_ge_sr)
                self.update_sk_es(sk, es_metric, n_profiling_traces)
                rs_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, search_index)

                print(colored("Computing Guessing Entropy and Success Rate for Validation Set", "green"))
                label_name = f"ES Validation Set {es_metric} {search_index} {n_profiling_traces} traces" if self.settings[
                    "use_profiling_analyzer"] else f"ES Validation Set {es_metric} {search_index}"
                random_states_ge_sr = random_states[f"{search_index}"][f"{label_name}"] if random_states is not None else None
                ge, sr, nt, sk, r = SCAMetrics(model, self.dataset.x_validation, self.settings, self.labels_key_guesses_validation_set).run(
                    random_states=random_states_ge_sr)
                rs_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, search_index)
                self.update_early_stopping_ge_and_sr(es_metric, ge, sr, n_profiling_traces)

                self.delete_model(es_metric)

    def finalize_search(self, profiling, model_descriptions, hp_ids, steps=None):

        """ Display results for best model """
        self.display_best_model()

        """ Update labels of best Guessing Entropy and Success Rate in database """
        if self.settings["use_early_stopping"]:
            early_stopping_metrics = self.get_early_stopping_metrics(
                profiling.get_builtin_callbacks()["early_stopping_callback"].get_metric_results())
        else:
            early_stopping_metrics = None
        if self.settings["use_profiling_analyzer"]:
            self.analysis_db_controls.update_best_model_metrics(self.best_model_index_pa, early_stopping_metrics, steps=steps)
        else:
            self.analysis_db_controls.update_best_model_metrics(self.best_model_index, early_stopping_metrics, steps=steps)

        """ Save model description (keras style) to database """
        if self.settings["use_profiling_analyzer"]:
            self.settings["best_hyperparameters_id"] = {}
            for n_profiling_traces in steps:
                best_model_index = self.best_model_index_pa[f"{n_profiling_traces}"]
                model_description = model_descriptions[best_model_index]
                self.analysis_db_controls.save_model_description_to_database(model_description, f"best_model_{best_model_index}",
                                                                             hp_ids[f"{n_profiling_traces}"][best_model_index])

                """ Update settings """
                self.settings["best_hyperparameters_id"][f"{n_profiling_traces}"] = hp_ids[f"{n_profiling_traces}"][
                    self.best_model_index_pa[f"{n_profiling_traces}"]]
            self.analysis_db_controls.db_update.db_update_settings(self.settings)
        else:
            best_model_index = self.best_model_index
            model_description = model_descriptions[best_model_index]
            self.analysis_db_controls.save_model_description_to_database(model_description, f"best_model_{best_model_index}",
                                                                         hp_ids[best_model_index])

            """ Update settings """
            self.settings["best_hyperparameters_id"] = hp_ids[int(best_model_index)]
            self.analysis_db_controls.db_update.db_update_settings(self.settings)

    def generate_model(self, hp_values):
        """ Generate a random/grid CNN or MLP model """
        if self.settings["use_grid_search"]:
            model, hp = self.generate_grid_model(hp_values)
        else:
            model, hp = self.generate_random_model(hp_values)
        self.hp_searches.append(hp)
        return model, hp
