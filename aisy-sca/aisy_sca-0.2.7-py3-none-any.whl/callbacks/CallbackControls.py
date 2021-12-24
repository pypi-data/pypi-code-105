from aisy_sca.callbacks.Callbacks import *
import importlib


class CallbackControls:

    def __init__(self, dataset, settings):
        self.settings = settings
        self.dataset = dataset
        self.callbacks = []
        self.builtin_callbacks = {}
        self.custom_callbacks_list = {}

    def add_callback(self, callback, name):
        self.callbacks.append(callback)
        self.builtin_callbacks[name] = callback
        return self.callbacks

    def add_custom_callback(self, callback, callback_name):
        self.custom_callbacks_list[callback_name] = callback

    def create_callbacks(self):
        """
            Initialize callbacks according to settings
            Callbacks can be:
            - Visualization callback for input gradients calculations (implemented in aisy_sca package)
            - Early stopping callbacks if user consider early-stopping metrics
            - Custom callbacks from user
        """

        self.callbacks = []
        if self.settings["use_visualization"]:
            """ Create visualization callback """
            self.add_callback(InputGradients(self.dataset, self.settings), "input_gradients_callback")

        if self.settings["use_early_stopping"]:
            """ Create early-stopping (user custom metrics) callbacks """
            self.add_callback(EarlyStoppingCallback(self.dataset, self.settings), "early_stopping_callback")

        if self.settings["use_confusion_matrix"]:
            """ Create confusion matrix callback """
            x = self.dataset.x_validation if self.dataset.x_validation is not None else self.dataset.x_attack
            y = self.dataset.y_validation if self.dataset.y_validation is not None else self.dataset.y_attack
            self.add_callback(ConfusionMatrix(x, y), "confusion_matrix_callback")

        if self.settings["use_custom_callbacks"]:

            """ Create user custom callbacks """
            for custom_callback in self.settings["custom_callbacks"]:
                callback_inverted = custom_callback['class'][::-1]
                module_name = callback_inverted.partition(".")[2][::-1]
                callback_name = callback_inverted.partition(".")[0][::-1]
                module_name = importlib.import_module(module_name)
                custom_callback_class = getattr(module_name, callback_name)
                custom_callback_obj = custom_callback_class(self.dataset, self.settings, custom_callback['parameters'])
                self.add_callback(custom_callback_obj, callback_name)
                self.add_custom_callback(custom_callback_obj, custom_callback['name'])

    def get_callbacks(self):
        return self.callbacks

    def get_builtin_callbacks(self):
        return self.builtin_callbacks

    def get_custom_callbacks(self):
        return self.custom_callbacks_list
