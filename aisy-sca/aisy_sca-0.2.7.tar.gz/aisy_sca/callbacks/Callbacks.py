from tensorflow.keras.callbacks import Callback
import tensorflow.keras.backend as backend
import tensorflow as tf
import numpy as np
import importlib
from sklearn.metrics import confusion_matrix
from termcolor import colored
import os


class EarlyStoppingCallback(Callback):
    def __init__(self, dataset, settings):
        super().__init__()
        self.dataset = dataset
        self.settings = settings
        self.metrics = settings["early_stopping"]["metrics"]
        self.timestamp = settings["timestamp"]

        self.metric_results = {}
        for metric in self.metrics:
            self.metric_results[metric] = []

    def on_epoch_end(self, epoch, logs={}):

        if self.metrics is not None:

            for metric in self.metrics:
                script = importlib.import_module(self.metrics[metric]["class"])
                metric_value = script.run(self.dataset, self.settings, self.model, self.metrics[metric]["parameters"])
                self.metric_results[metric].append(metric_value)

                if epoch > 0:
                    ref_value_epoch_list = None
                    ref_metric = None
                    if self.metrics[metric]["direction"] == "max":
                        if isinstance(metric_value, list):
                            ref_value_epoch_list = np.zeros(len(self.metric_results[metric][epoch]))
                            for index, current_epoch_value in enumerate(self.metric_results[metric][epoch]):
                                all_values_metric = []
                                for e in range(epoch):
                                    all_values_metric.append(self.metric_results[metric][e][index])
                                ref_value_epoch_list[index] = np.max(all_values_metric)
                        else:
                            ref_metric = np.max(self.metric_results[metric][0:epoch])
                    else:
                        if isinstance(metric_value, list):
                            ref_value_epoch_list = np.zeros(len(self.metric_results[metric][epoch]))
                            for index, current_epoch_value in enumerate(self.metric_results[metric][epoch]):
                                all_values_metric = []
                                for e in range(epoch):
                                    all_values_metric.append(self.metric_results[metric][e][index])
                                ref_value_epoch_list[index] = np.min(all_values_metric)
                        else:
                            ref_metric = np.min(self.metric_results[metric][0:epoch])

                    if isinstance(metric_value, list):
                        for index, current_epoch_value in enumerate(self.metric_results[metric][epoch]):
                            if (self.metric_results[metric][epoch][index] > ref_value_epoch_list[index] and self.metrics[metric][
                                "direction"] == "max") or (
                                    self.metric_results[metric][epoch][index] < ref_value_epoch_list[index] and self.metrics[metric][
                                "direction"] == "min"):
                                model_name = f"{self.settings['resources_root_folder']}models/best_model_{metric}_{self.settings['timestamp']}_{index}.h5"
                                os.remove(model_name)
                                self.model.save_weights(model_name)
                                print(
                                    colored(f"\nModel saved {metric} = {self.metric_results[metric][epoch][index]} at epoch {epoch + 1}\n",
                                            "blue"))
                    else:
                        if (self.metric_results[metric][epoch] > ref_metric and self.metrics[metric]["direction"] == "max") or (
                                self.metric_results[metric][epoch] < ref_metric and self.metrics[metric]["direction"] == "min"):
                            model_name = f"{self.settings['resources_root_folder']}models/best_model_{metric}_{self.settings['timestamp']}.h5"
                            os.remove(model_name)
                            self.model.save_weights(model_name)
                            print(colored(f"\nModel saved {metric} = {self.metric_results[metric][epoch]} at epoch {epoch + 1}\n", "blue"))
                else:
                    if isinstance(metric_value, list):
                        for index, current_epoch_value in enumerate(self.metric_results[metric][epoch]):
                            model_name = f"{self.settings['resources_root_folder']}models/best_model_{metric}_{self.settings['timestamp']}_{index}.h5"
                            self.model.save_weights(model_name)
                            print(
                                colored(f"\nModel saved {metric} = {self.metric_results[metric][epoch][index]} at epoch {epoch + 1}\n",
                                        "blue"))
                    else:
                        model_name = f"{self.settings['resources_root_folder']}models/best_model_{metric}_{self.settings['timestamp']}.h5"
                        self.model.save_weights(model_name)
                        print(colored(f"\nModel saved {metric} = {self.metric_results[metric][epoch]} at epoch {epoch + 1}\n", "blue"))

    def get_metric_results(self):
        return self.metric_results


class InputGradients(Callback):
    def __init__(self, dataset, settings):
        super().__init__()
        self.current_epoch = 0
        self.x = dataset.x_profiling[:settings["visualization"]]
        self.y = dataset.y_profiling[:settings["visualization"]]
        self.number_of_epochs = settings["epochs"]
        self.number_of_samples = settings["number_of_samples"]
        self.gradients = np.zeros((settings["epochs"], settings["number_of_samples"]))
        self.gradients_sum = np.zeros(settings["number_of_samples"])

    def on_epoch_end(self, epoch, logs=None):
        input_trace = tf.Variable(self.x)

        with tf.GradientTape() as tape:
            tape.watch(input_trace)
            pred = self.model(input_trace)
            loss = tf.keras.losses.categorical_crossentropy(self.y, pred)

        grad = tape.gradient(loss, input_trace)

        input_gradients = np.zeros(self.number_of_samples)
        for i in range(len(self.x)):
            input_gradients += grad[i].numpy().reshape(self.number_of_samples)

        self.gradients[epoch] = input_gradients
        if np.max(self.gradients[epoch]) != 0:
            self.gradients_sum += np.abs(self.gradients[epoch] / np.max(self.gradients[epoch]))
        else:
            self.gradients_sum += np.abs(self.gradients[epoch])

        backend.clear_session()

    def input_gradients_sum(self):
        return np.abs(self.gradients_sum)

    def input_gradients_epochs(self):
        for e in range(self.number_of_epochs):
            if np.max(self.gradients[e]) != 0:
                self.gradients[e] = np.abs(self.gradients[e] / np.max(self.gradients[e]))
            else:
                self.gradients[e] = np.abs(self.gradients[e])
        return self.gradients


class ConfusionMatrix(Callback):
    def __init__(self, x, y):
        super().__init__()
        self.current_epoch = 0
        self.x = x
        self.y_true = np.argmax(y, axis=1)
        self.cm = None

    def on_epoch_end(self, epoch, logs=None):
        Y_pred = self.model.predict(self.x)
        y_pred = np.argmax(Y_pred, axis=1)
        self.cm = confusion_matrix(y_true=self.y_true, y_pred=y_pred)

    def get_confusion_matrix(self):
        return self.cm
