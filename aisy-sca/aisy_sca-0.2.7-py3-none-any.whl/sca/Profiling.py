from aisy_sca.callbacks.CallbackControls import CallbackControls
from aisy_sca.metrics import SCAMetrics
import tensorflow.keras.backend as backend
from termcolor import colored
import numpy as np
import os


class Profiling:
    """
    Class to run profiling phase on the dataset and model
    model: keras model already compiled
    settings: analysis settings
    dataset: dataset structure containing traces, labels and metadata (plaintext, ciphertext, keys)
    search_index: for hyper-parameter search purposes
    train_best_model: for hyper-parameter search purposes
    """

    def __init__(self, settings, dataset, da_function):
        self.settings = settings
        self.dataset = dataset
        self.da_function = da_function
        self.builtin_callbacks = None
        self.custom_callbacks = None
        self.labels_key_guesses_attack_set = None
        self.labels_key_guesses_validation_set = None

    def train_model(self, model, n_profiling_traces=None):

        """
        Train the model (profiling phase).
        1. Configure dataset
        2. Train model
        """

        """ reshape traces if needed """
        input_layer_shape = model.get_layer(index=0).input_shape

        """ Check if model is created with Sequential or Model class from Keras """
        if len(input_layer_shape) == 1:
            """ Model was created with Model class """
            input_layer_shape = input_layer_shape[0]

        """ Check if neural network is a cnn or mlp """
        if len(input_layer_shape) == 3:
            self.dataset.reshape_for_cnn()
        else:
            self.dataset.reshape_for_mlp()

        """ Create callbacks """
        callback_controls = CallbackControls(self.dataset, self.settings)
        callback_controls.create_callbacks()
        callbacks = callback_controls.get_callbacks()
        self.builtin_callbacks = callback_controls.get_builtin_callbacks()
        self.custom_callbacks = callback_controls.get_custom_callbacks()

        if self.settings["split_test_set"] or self.settings["split_training_set"]:
            validation_set = (self.dataset.x_validation, self.dataset.y_validation)
        else:
            validation_set = (self.dataset.x_attack, self.dataset.y_attack)

        if self.settings["use_data_augmentation"]:

            """  If data augmentation is used, then x_profiling needs to be reshaped back to 2D. """

            x_profiling = self.dataset.x_profiling.reshape((self.dataset.x_profiling.shape[0], self.dataset.x_profiling.shape[1]))

            da_method = self.da_function(x_profiling, self.dataset.y_profiling, self.settings["batch_size"], input_layer_shape)
            history = model.fit_generator(
                generator=da_method,
                steps_per_epoch=self.settings["data_augmentation"][1],
                epochs=self.settings["epochs"],
                verbose=2,
                validation_data=validation_set,
                validation_steps=1,
                callbacks=callbacks)

        else:

            """ Train the model """

            history = model.fit(
                x=self.dataset.x_profiling[:n_profiling_traces] if self.settings["use_profiling_analyzer"] else self.dataset.x_profiling,
                y=self.dataset.y_profiling[:n_profiling_traces] if self.settings["use_profiling_analyzer"] else self.dataset.y_profiling,
                batch_size=self.settings["batch_size"],
                verbose=2,
                epochs=self.settings["epochs"],
                shuffle=True,
                validation_data=validation_set,
                callbacks=callbacks)

        return history

    def get_builtin_callbacks(self):
        return self.builtin_callbacks

    def get_custom_callbacks(self):
        return self.custom_callbacks

    def compute_metrics(self, model, analysis_db_controls, hp_id, n_profiling_traces=None, random_states=None):

        """ Compute SCA metrics: guessing entropy and success rate for attack and validation sets """

        """ 
        Compute Guessing Entropy, Success Rate and Number of Traces for Success (GE < 2) for attack and validation sets 
        Return scores/probabilities for each trace (p(l=leakage|trace=x))
        Retrieve random states for reproducibility
        Save results to database
        """

        label_name = f"Attack Set" if n_profiling_traces is None else f"Attack Set {n_profiling_traces} traces"
        random_states_ge_sr = random_states[f"{model['index']}"][f"{label_name}"] if random_states is not None else None
        ge, sr, nt, sk, r = SCAMetrics(model["model"], self.dataset.x_attack, self.settings, self.labels_key_guesses_attack_set).run(
            random_states=random_states_ge_sr)

        analysis_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, model['index'])

        if self.dataset.x_validation is not None:
            label_name = f"Validation Set" if n_profiling_traces is None else f"Validation Set {n_profiling_traces} traces"
            random_states_ge_sr = random_states[f"{model['index']}"][f"{label_name}"] if random_states is not None else None
            ge, sr, nt, sk, r = SCAMetrics(model["model"], self.dataset.x_validation, self.settings,
                                           self.labels_key_guesses_validation_set).run(
                random_states=random_states_ge_sr)
            analysis_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, model['index'])

        """
        For Early Stopping Metrics:
        Compute Guessing Entropy, Success Rate and Number of Traces for Success (GE < 2) for attack and validation sets 
        Return scores/probabilities for each trace (p(l=leakage|trace=x))
        Retrieve random states for reproducibility        
        """

        """ TODO: search for saved h5 models in folder and then run metrics"""

        if self.settings["use_early_stopping"]:

            early_stopping_metrics = self.get_early_stopping_metrics(
                self.builtin_callbacks["early_stopping_callback"].get_metric_results())

            for es_metric in early_stopping_metrics:
                self.load_model(model["model"], es_metric)

                print(colored("Computing Guessing Entropy and Success Rate for Attack Set", "green"))
                label_name = f"ES Attack Set {es_metric}" if n_profiling_traces is None else f"ES Attack Set {es_metric} {n_profiling_traces} traces"
                random_states_ge_sr = random_states[f"{model['index']}"][f"{label_name}"] if random_states is not None else None
                ge, sr, nt, sk, r = SCAMetrics(model["model"], self.dataset.x_attack, self.settings,
                                               self.labels_key_guesses_attack_set).run(
                    random_states=random_states_ge_sr)
                analysis_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, model['index'])

                print(colored("Computing Guessing Entropy and Success Rate for Validation Set", "green"))
                label_name = f"ES Validation Set {es_metric}" if n_profiling_traces is None else f"ES Validation Set {es_metric} {n_profiling_traces} traces"
                random_states_ge_sr = random_states[f"{model['index']}"][f"{label_name}"] if random_states is not None else None
                ge, sr, nt, sk, r = SCAMetrics(model["model"], self.dataset.x_validation, self.settings,
                                               self.labels_key_guesses_validation_set).run(
                    random_states=random_states_ge_sr)
                analysis_db_controls.save_sca_metrics_to_database(ge, sr, label_name, hp_id, r, model['index'])

                self.delete_model(es_metric)

    def load_model(self, model, setting, idx=None):

        """ Load weights from saved early stopping model from 'resource/models' directory"""

        if idx is None:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}.h5"
        else:
            model_name = f"{self.settings['resources_root_folder']}models/best_model_{setting}_{self.settings['timestamp']}_{idx}.h5"
        print(model_name)
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
