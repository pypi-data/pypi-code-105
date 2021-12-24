from aisy_sca.optimization.RandomGridSearch import RandomGridSearch
from aisy_sca.optimization.ProfilingAnalyzer import ProfilingAnalyzer
from aisy_sca.optimization.Ensemble import Ensemble
from aisy_sca.AnalysisDatabaseControls import *
from aisy_sca.LeakageModelControls import *


class HyperparameterSearchProcess:

    def __init__(self, dataset, settings, models, da_function, hp_combinations_reproducible, labels_key_guesses_attack_set=None,
                 labels_key_guesses_validation_set=None, loss_function=None, random_states=None):
        self.dataset = dataset
        self.settings = settings
        self.models = models
        self.da_function = da_function
        self.hp_combinations_reproducible = hp_combinations_reproducible
        self.custom_callbacks = None
        self.labels_key_guesses_attack_set = labels_key_guesses_attack_set
        self.labels_key_guesses_validation_set = labels_key_guesses_validation_set
        self.loss_function = loss_function
        self.random_states = random_states

    def run(self):

        """ Create analysis in database """
        analysis_db_controls = AnalysisDatabaseControls(self.settings)
        self.settings["analysis_id"] = analysis_db_controls.analysis_id
        analysis_db_controls.save_leakage_model_to_database()

        """ Generate list of labels for all key guesses for validation and attack sets """
        if self.labels_key_guesses_attack_set is None and self.labels_key_guesses_validation_set is None:
            lm_control = LeakageModelControls(self.settings)
            self.labels_key_guesses_attack_set, self.labels_key_guesses_validation_set = lm_control.compute_labels_key_guesses(self.dataset)

        """ Create random search process"""
        if self.settings["use_random_search"]:
            search_settings = self.settings["random_search"]
        else:
            search_settings = self.settings["grid_search"]

        if self.settings["use_profiling_analyzer"]:
            hp_search = ProfilingAnalyzer(self.settings, self.dataset, search_settings, self.labels_key_guesses_attack_set,
                                          self.labels_key_guesses_validation_set, analysis_db_controls, random_states=self.random_states)
            hp_search.loss_function = self.loss_function
            hp_search.run(self.hp_combinations_reproducible, da_function=self.da_function, grid_search=self.settings["use_grid_search"])
            self.custom_callbacks = hp_search.get_custom_callbacks()
        else:
            hp_search = RandomGridSearch(self.settings, self.dataset, search_settings, self.labels_key_guesses_attack_set,
                                         self.labels_key_guesses_validation_set, analysis_db_controls, random_states=self.random_states)
            hp_search.loss_function = self.loss_function
            hp_search.run(self.hp_combinations_reproducible, da_function=self.da_function, grid_search=self.settings["use_grid_search"])
            self.custom_callbacks = hp_search.get_custom_callbacks()

        """ Compute Ensembles"""
        if self.settings["use_ensemble"]:
            ensembles = Ensemble(self.settings, self.dataset)
            if self.settings["use_profiling_analyzer"]:
                for n_profiling_traces in self.settings["profiling_analyzer_steps"]:
                    ensembles.compute(hp_search.get_sk_attack_pa()[f"{n_profiling_traces}"], self.settings["ensemble"][0],
                                      self.labels_key_guesses_attack_set, analysis_db_controls, n_profiling=n_profiling_traces)
            else:
                ensembles.compute(hp_search.get_sk_attack(), self.settings["ensemble"][0], self.labels_key_guesses_attack_set,
                                  analysis_db_controls)
            if self.settings["use_early_stopping"]:
                for metric in self.settings["early_stopping"]["metrics"]:
                    if self.settings["use_profiling_analyzer"]:
                        for n_profiling_traces in self.settings["profiling_analyzer_steps"]:
                            ensembles.compute(hp_search.get_sk_attack_es()[metric][f"{n_profiling_traces}"],
                                              self.settings["ensemble"][0], self.labels_key_guesses_attack_set,
                                              analysis_db_controls, early_stopping_metric=metric, n_profiling=n_profiling_traces)
                    else:
                        ensembles.compute(hp_search.get_sk_attack_es()[metric], self.settings["ensemble"][0],
                                          self.labels_key_guesses_attack_set, analysis_db_controls, early_stopping_metric=metric)

    def get_custom_callbacks(self):
        return self.custom_callbacks
