from aisy_sca.sca.Profiling import Profiling
from aisy_sca.utils.utils import Utils
import tensorflow.keras.backend as backend
import time


class SingleModel(Profiling):

    def __init__(self, settings, dataset, da_function, random_states=None):
        super().__init__(settings, dataset, da_function)
        self.settings = settings
        self.dataset = dataset
        self.da_function = da_function
        self.labels_key_guesses_attack_set = None
        self.labels_key_guesses_validation_set = None
        self.analysis_db_controls = None
        self.custom_callbacks = None
        self.random_states = random_states

    def run(self, model):

        initial_weights = model["model"].get_weights()
        model["model"].summary()

        start = time.time()

        hp_id = None

        for idx, n_profiling in enumerate(self.settings["profiling_analyzer_steps"]):

            """ Run profiling/training phase """

            model["model"].set_weights(initial_weights)
            history = self.train_model(model["model"], n_profiling_traces=n_profiling)
            self.custom_callbacks = self.get_custom_callbacks()

            """ Save hyper-parameters combination to database """
            if idx == 0:
                hyper_parameters_list = Utils().get_hyperparameters_from_model(model["model"])
                hp_id = self.analysis_db_controls.save_hyper_parameters_to_database(hyper_parameters_list)

            """ Retrieve metrics from model and save them to database """
            if self.settings["use_early_stopping"]:
                early_stopping_metrics = self.get_early_stopping_metrics(
                    self.get_builtin_callbacks()["early_stopping_callback"].get_metric_results())
                early_stopping_epoch_values = self.get_early_stopping_values_epochs(
                    self.get_builtin_callbacks()["early_stopping_callback"].get_metric_results())
            else:
                early_stopping_metrics = None
                early_stopping_epoch_values = None
            self.analysis_db_controls.save_generic_metrics(history, early_stopping_metrics, early_stopping_epoch_values, hp_id,
                                                           n_profiling_traces=n_profiling if self.settings[
                                                               "use_profiling_analyzer"] else None)

            """ Compute SCA metrics and save them to database """
            self.compute_metrics(model, self.analysis_db_controls, hp_id,
                                 n_profiling_traces=n_profiling if self.settings["use_profiling_analyzer"] else None,
                                 random_states=self.random_states)

            """ Save model description (keras style) to database """
            model_description = Utils().keras_model_as_string(model["model"], model["method_name"])
            self.analysis_db_controls.save_model_description_to_database(model_description, model["method_name"], hp_id)

            """ Save visualization results to database """
            if self.settings["use_visualization"]:
                self.analysis_db_controls.save_visualization_results_to_database(
                    self.get_builtin_callbacks()["input_gradients_callback"].input_gradients_epochs(),
                    self.get_builtin_callbacks()["input_gradients_callback"].input_gradients_sum(), hp_id)

            """ Save confusion matrix results to database """
            if self.settings["use_confusion_matrix"]:
                self.analysis_db_controls.save_confusion_matrix_results_to_database(
                    self.get_builtin_callbacks()["confusion_matrix_callback"].get_confusion_matrix(), hp_id)

            """ update database settings"""
            self.analysis_db_controls.update_results_in_database(time.time() - start)

            backend.clear_session()
