from aisy_sca.utils import Utils
from aisy_sca.datasets import DatasetControls
from aisy_sca.AnalysisControls import *
from aisy_sca.analysis.SingleProcess import SingleProcess
from aisy_sca.analysis.HyperparameterSearchProcess import HyperparameterSearchProcess
from aisy_sca.LeakageModelControls import *
from numpy.random import seed as numpy_seed
import tensorflow.keras.backend as backend
import tensorflow as tf
import inspect
import importlib
import time


class Aisy:

    def __init__(self):

        """ variables for analysis"""
        self.settings = {}
        self.dataset = None
        self.models = {}
        self.custom_callbacks = None
        self.loss_function = None

        """ variables from external datasets """
        self.labels_key_guesses_attack_set = None
        self.labels_key_guesses_validation_set = None

        """ reproducibility """
        self.random_states = None
        self.hyperparameters_reproducible = None

    def run(self, key_rank_executions=100, key_rank_report_interval=10, key_rank_attack_traces=1000, visualization=None,
            data_augmentation=None, ensemble=None, grid_search=None, random_search=None, early_stopping=None, confusion_matrix=False,
            callbacks=None, profiling_analyzer=None):

        """
        Main AISY framework function. This function runs neural network training for profiled side-channel analysis in a known-key setting.
        """

        self.settings["key_rank_executions"] = key_rank_executions
        self.settings["key_rank_attack_traces"] = key_rank_attack_traces
        self.settings["key_rank_report_interval"] = key_rank_report_interval
        self.settings["timestamp"] = str(time.time()).replace(".", "")

        analysis_controls = AnalysisControls(self.settings, self.models)
        analysis_controls.update_settings(random_search, grid_search, visualization, early_stopping, data_augmentation, callbacks, ensemble,
                                          confusion_matrix, profiling_analyzer)
        analysis_controls.check_errors()
        da_function = data_augmentation[0] if data_augmentation is not None else None

        """ Load data sets """
        if self.dataset is None:
            ds_controls = DatasetControls(self.settings)
            ds_controls.read()
            self.dataset = ds_controls.get_dataset()

        """ Run main process """
        if self.settings["hyperparameter_search"]:
            hyperparameter_search_process = HyperparameterSearchProcess(
                self.dataset, self.settings, self.models, da_function, self.hyperparameters_reproducible,
                labels_key_guesses_attack_set=self.labels_key_guesses_attack_set,
                labels_key_guesses_validation_set=self.labels_key_guesses_validation_set,
                loss_function=self.loss_function, random_states=self.random_states)
            hyperparameter_search_process.run()

            """ Get custom callbacks """
            self.custom_callbacks = hyperparameter_search_process.custom_callbacks
        else:
            single_process = SingleProcess(
                self.dataset, self.settings, self.models, da_function,
                labels_key_guesses_attack_set=self.labels_key_guesses_attack_set,
                labels_key_guesses_validation_set=self.labels_key_guesses_validation_set,
                random_states=self.random_states)
            single_process.run()

            """ Get custom callbacks """
            self.custom_callbacks = single_process.custom_callbacks

    def set_datasets_root_folder(self, datasets_root_folder):
        self.settings["datasets_root_folder"] = Utils().adapt_folder_path(datasets_root_folder)

    def set_database_root_folder(self, database_root_folder):
        self.settings["database_root_folder"] = Utils().adapt_folder_path(database_root_folder)

    def set_resources_root_folder(self, resources_root_folder):
        self.settings["resources_root_folder"] = Utils().adapt_folder_path(resources_root_folder)

    def set_dataset_filename(self, dataset_filename):
        self.settings["filename"] = dataset_filename

    def set_first_sample(self, first_sample):
        self.settings["first_sample"] = first_sample

    def set_number_of_samples(self, number_of_samples):
        self.settings["number_of_samples"] = number_of_samples

    def set_number_of_profiling_traces(self, profiling_traces):
        self.settings["number_of_profiling_traces"] = profiling_traces

    def set_number_of_attack_traces(self, attack_traces):
        self.settings["number_of_attack_traces"] = attack_traces

    def set_key(self, key):
        self.settings["key"] = key

    def set_dataset(self, target_dict, dataset=None):
        for key, value in target_dict.items():
            self.settings[str(key)] = value
        if dataset is not None:
            self.dataset = dataset

    def set_database_name(self, database_name):
        self.settings["database_name"] = database_name

    def set_batch_size(self, batch_size):
        self.settings["batch_size"] = batch_size

    def set_epochs(self, epochs):
        self.settings["epochs"] = epochs

    def set_hyperparameters_reproducible(self, hyperparameters_reproducible):
        self.hyperparameters_reproducible = hyperparameters_reproducible

    def set_random_states(self, random_states):
        self.random_states = random_states

    def get_models(self):
        return self.models

    def set_model_weights(self, weights, model_index=0):
        self.models[f"{model_index}"].set_weights(weights)

    def set_neural_network(self, model, name=None):
        self.add_neural_network(model, name=name)

    def add_neural_network(self, model, name=None, seed=None):
        if not bool(self.models):
            self.settings["models"] = {}
        model_index = len(self.models)
        if inspect.isfunction(model):
            model_name = model.__name__ if name is None else name
            tf_random_seed = np.random.randint(1048576) if seed is None else seed
            tf.random.set_seed(tf_random_seed)
            method_name = model.__name__
            model = model(self.settings["classes"], self.settings["number_of_samples"])
            self.__set_model_attributes(model_index, model_name, method_name, tf_random_seed, model)
        else:
            self.__set_model_attributes(model_index, model.name if name is None else name, model.name, seed, model)

    def __set_model_attributes(self, model_index, model_name, method_name, seed, model):

        self.models[f"{model_index}"] = {}
        self.models[f"{model_index}"]["model_name"] = model_name
        self.models[f"{model_index}"]["method_name"] = method_name
        self.models[f"{model_index}"]["seed"] = seed
        self.models[f"{model_index}"]["model"] = model
        self.models[f"{model_index}"]["index"] = model_index

        self.settings["models"][f"{model_index}"] = {}
        self.settings["models"][f"{model_index}"]["model_name"] = model_name
        self.settings["models"][f"{model_index}"]["method_name"] = method_name
        self.settings["models"][f"{model_index}"]["seed"] = seed
        self.settings["models"][f"{model_index}"]["index"] = model_index

    def set_loss_function(self, loss_dict, model_args=None):

        self.loss_function = loss_dict

        class_inverted = loss_dict["class"][::-1]
        module_name = class_inverted.partition(".")[2][::-1]
        loss_function_name = class_inverted.partition(".")[0][::-1]
        module_name = importlib.import_module(module_name)
        custom_loss_class = getattr(module_name, loss_function_name)

        if model_args is not None:
            if len(model_args) != len(self.models):
                print("Expected args to be a list with same amount of models.")
                return

        for model_index, model in self.models.items():
            learning_rate = backend.eval(model["model"].optimizer.lr)
            optimizer = model["model"].optimizer.__class__
            if model_args is not None:
                m_args = model_args[int(model_index)]
            else:
                m_args = None
            model["model"].compile(
                loss=custom_loss_class(self.settings, model_args=m_args, parameters=loss_dict['parameters']),
                optimizer=optimizer(learning_rate=learning_rate), metrics=['accuracy'])

    def set_aes_leakage_model(self, leakage_model="HW", bit=0, byte=0, round=1, round_first=1, round_second=1, cipher="AES128",
                              target_state="Sbox", target_state_first="Sbox", target_state_second="Sbox",
                              direction="Encryption", attack_direction="input"):
        lm_control = LeakageModelControls(self.settings)
        self.settings = lm_control.set(leakage_model, bit, byte, round, round_first, round_second, cipher, target_state, target_state_first,
                                       target_state_second, direction, attack_direction)
        self.settings["good_key"] = bytearray.fromhex(self.settings["key"])[self.settings["leakage_model"]["byte"]]

    def set_good_key(self, key):
        self.settings["good_key"] = int(key)

    def set_classes(self, classes):
        self.settings["classes"] = classes

    def set_labels_key_guesses_attack_set(self, labels_key_guesses_attack_set):
        self.labels_key_guesses_attack_set = labels_key_guesses_attack_set

    def set_labels_key_guesses_validation_set(self, labels_key_guesses_validation_set):
        self.labels_key_guesses_validation_set = labels_key_guesses_validation_set

    def get_custom_callbacks(self):
        return self.custom_callbacks
