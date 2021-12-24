from tensorflow.keras.optimizers import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow as tf
import numpy as np
import random
import importlib


class KerasCNNRandom:

    def __init__(self, settings, hyperparameters, fixed_model=False, loss_function=None):
        self.settings = settings
        self.hyperparameters = hyperparameters
        self.model_structure = settings["random_search"]["structure"]
        self.fixed_model = fixed_model
        self.loss_function = loss_function

    def cnn_random_search(self):
        if self.fixed_model:
            conv_layers = self.hyperparameters["conv_layers"] if "conv_layers" in self.hyperparameters else 1
            kernels = []
            strides = []
            filters = []
            pooling_types = []
            pooling_layers = []
            pooling_sizes = []
            pooling_strides = []
            for conv_layer in range(1, conv_layers + 1):
                kernels.append(
                    self.hyperparameters["kernel_{}".format(conv_layer)] if "kernel_{}".format(conv_layer) in self.hyperparameters else 4)
                strides.append(
                    self.hyperparameters["stride_{}".format(conv_layer)] if "stride_{}".format(conv_layer) in self.hyperparameters else 1)
                filters.append(self.hyperparameters["filters_{}".format(conv_layer)] if "filters_{}".format(
                    conv_layer) in self.hyperparameters else 16)
                pooling_sizes.append(
                    self.hyperparameters["pooling_size_{}".format(conv_layer)] if "pooling_size_{}".format(
                        conv_layer) in self.hyperparameters else 2)
                pooling_strides.append(
                    self.hyperparameters["pooling_stride_{}".format(conv_layer)] if "pooling_stride_{}".format(
                        conv_layer) in self.hyperparameters else 2)
                pooling_types.append(
                    self.hyperparameters["pooling_type_{}".format(conv_layer)] if "pooling_type_{}".format(
                        conv_layer) in self.hyperparameters else "Average")
                if pooling_types[conv_layer - 1] == "Average":
                    pooling_layers.append(
                        AveragePooling1D(pool_size=pooling_sizes[conv_layer - 1], strides=pooling_strides[conv_layer - 1]))
                elif pooling_types[conv_layer - 1] == "Max":
                    pooling_layers.append(MaxPool1D(pool_size=pooling_sizes[conv_layer - 1], strides=pooling_strides[conv_layer - 1]))
                else:
                    pooling_layers.append(
                        AveragePooling1D(pool_size=pooling_sizes[conv_layer - 1], strides=pooling_strides[conv_layer - 1]))

            neurons = self.hyperparameters["neurons"] if "neurons" in self.hyperparameters else 50
            layers = self.hyperparameters["layers"] if "layers" in self.hyperparameters else 5
            activation = self.hyperparameters["activation"] if "activation" in self.hyperparameters else "relu"
            learning_rate = self.hyperparameters["learning_rate"] if "learning_rate" in self.hyperparameters else 0.001
            optimizer = self.hyperparameters["optimizer"] if "optimizer" in self.hyperparameters else "Adam"
            dropout_rate = self.hyperparameters["dropout_rate"] if "dropout_rate" in self.hyperparameters else 0
            random_seed = self.hyperparameters["seed"] if "seed" in self.hyperparameters else np.random.randint(1048576)

        else:
            conv_layers = random.randrange(self.hyperparameters["conv_layers"]["min"],
                                           self.hyperparameters["conv_layers"]["max"] + self.hyperparameters["conv_layers"]["step"],
                                           self.hyperparameters["conv_layers"]["step"]) if "conv_layers" in self.hyperparameters else 1
            kernels = []
            strides = []
            filters = []
            pooling_types = []
            pooling_sizes = []
            pooling_strides = []
            for conv_layer in range(1, conv_layers + 1):
                filters = self.get_convolution_hyperparameter(conv_layer, filters, "filters")
                kernels = self.get_convolution_hyperparameter(conv_layer, kernels, "kernel")
                strides = self.get_convolution_hyperparameter(conv_layer, strides, "stride")
                pooling_sizes = self.get_pooling_hyperparameter(conv_layer, pooling_sizes, "size")
                pooling_strides = self.get_pooling_hyperparameter(conv_layer, pooling_strides, "stride")
                pooling_types = self.get_pooling_type(conv_layer, pooling_types)

            # set default values if not present in hyper_parameters_ranges
            neurons = random.randrange(self.hyperparameters["neurons"]["min"],
                                       self.hyperparameters["neurons"]["max"] + self.hyperparameters["neurons"]["step"],
                                       self.hyperparameters["neurons"]["step"]) if "neurons" in self.hyperparameters else 50
            layers = random.randrange(self.hyperparameters["layers"]["min"],
                                      self.hyperparameters["layers"]["max"] + self.hyperparameters["layers"]["step"],
                                      self.hyperparameters["layers"]["step"]) if "layers" in self.hyperparameters else 5
            activation = random.choice(self.hyperparameters["activation"]) if "activation" in self.hyperparameters else "relu"
            learning_rate = random.choice(self.hyperparameters["learning_rate"]) if "learning_rate" in self.hyperparameters else 0.001
            optimizer = random.choice(self.hyperparameters["optimizer"])
            if self.model_structure["use_dropout_after_dense_layer"] or self.model_structure["use_dropout_before_dense_layer"]:
                dropout_rate = random.choice(self.hyperparameters["dropout_rate"])
            else:
                dropout_rate = 0
            random_seed = np.random.randint(1048576)

        hp = {'conv_layers': conv_layers}
        for conv_layer in range(1, conv_layers + 1):
            hp["kernel_{}".format(conv_layer)] = kernels[conv_layer - 1]
            hp["stride_{}".format(conv_layer)] = strides[conv_layer - 1]
            hp["filters_{}".format(conv_layer)] = filters[conv_layer - 1]
            hp["pooling_size_{}".format(conv_layer)] = pooling_sizes[conv_layer - 1]
            hp["pooling_stride_{}".format(conv_layer)] = pooling_strides[conv_layer - 1]
            hp["pooling_type_{}".format(conv_layer)] = pooling_types[conv_layer - 1]
        hp["neurons"] = neurons
        hp["layers"] = layers
        hp["activation"] = activation
        hp["learning_rate"] = learning_rate
        if self.model_structure["use_dropout_after_dense_layer"] or self.model_structure["use_dropout_before_dense_layer"]:
            hp["dropout_rate"] = dropout_rate
        hp["optimizer"] = optimizer
        hp["seed"] = random_seed

        tf.random.set_seed(random_seed)

        model = Sequential()
        for conv_layer in range(1, conv_layers + 1):
            if conv_layer == 1:

                if self.model_structure["use_pooling_before_first_convolution"]:

                    if "pooling_size_0" in self.hyperparameters and "pooling_stride_0" in self.hyperparameters and "pooling_type_0" in self.hyperparameters:

                        pooling_sizes_0 = random.randrange(self.hyperparameters["pooling_size_0"]["min"],
                                                           self.hyperparameters["pooling_size_0"]["max"] +
                                                           self.hyperparameters["pooling_size_0"]["step"],
                                                           self.hyperparameters["pooling_size_0"]["step"])
                        pooling_stride_0 = random.randrange(self.hyperparameters["pooling_stride_0"]["min"],
                                                            self.hyperparameters["pooling_stride_0"]["max"] +
                                                            self.hyperparameters["pooling_stride_0"][
                                                                "step"],
                                                            self.hyperparameters["pooling_stride_0"]["step"])
                        pooling_type_0 = random.choice(self.hyperparameters["pooling_type_0"])

                        if pooling_type_0 == "average":
                            model.add(AveragePooling1D(pool_size=pooling_sizes_0, strides=pooling_stride_0),
                                      input_shape=(self.settings["number_of_samples"], 1))
                        else:
                            model.add(MaxPool1D(pool_size=pooling_sizes_0, strides=pooling_stride_0,
                                                input_shape=(self.settings["number_of_samples"], 1)))

                        hp["pooling_size_0"] = pooling_sizes_0
                        hp["pooling_stride_0"] = pooling_stride_0
                        hp["pooling_type_0"] = pooling_type_0

                    model.add(
                        Conv1D(kernel_size=kernels[conv_layer - 1], strides=strides[conv_layer - 1], filters=filters[conv_layer - 1],
                               activation=activation, padding="same"))
                else:
                    model.add(
                        Conv1D(kernel_size=kernels[conv_layer - 1], strides=strides[conv_layer - 1], filters=filters[conv_layer - 1],
                               activation=activation, padding="same", input_shape=(self.settings["number_of_samples"], 1)))
            else:
                model.add(
                    Conv1D(kernel_size=kernels[conv_layer - 1], strides=strides[conv_layer - 1], filters=filters[conv_layer - 1],
                           activation=activation, padding="same"))
            if self.model_structure["use_batch_norm_after_convolution"] or (
                    self.model_structure["use_batch_norm_before_pooling"] and self.model_structure["use_pooling_after_convolution"]):
                model.add(BatchNormalization())
            if self.model_structure["use_pooling_after_convolution"]:
                if pooling_types[conv_layer - 1] == "average":
                    model.add(AveragePooling1D(pool_size=pooling_sizes[conv_layer - 1], strides=pooling_strides[conv_layer - 1]))
                else:
                    model.add(MaxPool1D(pool_size=pooling_sizes[conv_layer - 1], strides=pooling_strides[conv_layer - 1]))
            if self.model_structure["use_batch_norm_after_pooling"]:
                model.add(BatchNormalization())
        model.add(Flatten())
        for layer_index in range(layers):
            if self.model_structure["use_dropout_before_dense_layer"]:
                model.add(Dropout(dropout_rate))
            model.add(Dense(neurons, activation=activation))
            if self.model_structure["use_dropout_after_dense_layer"]:
                model.add(Dropout(dropout_rate))
        if self.model_structure["use_dropout_before_dense_layer"]:
            model.add(Dropout(dropout_rate))
        model.add(Dense(self.settings["classes"], activation='softmax'))
        model.summary()

        if self.loss_function is not None:
            class_inverted = self.loss_function["class"][::-1]
            module_name = class_inverted.partition(".")[2][::-1]
            loss_function_name = class_inverted.partition(".")[0][::-1]
            module_name = importlib.import_module(module_name)
            custom_loss_class = getattr(module_name, loss_function_name)
            loss = custom_loss_class(self.settings, parameters=self.loss_function['parameters'])
            model.compile(loss=loss, optimizer=self.get_optimizer(optimizer, learning_rate), metrics=['accuracy'])
        else:
            model.compile(loss='categorical_crossentropy', optimizer=self.get_optimizer(optimizer, learning_rate), metrics=['accuracy'])
        return model, hp

    def get_optimizer(self, optimizer, learning_rate):
        if optimizer == "Adam":
            return Adam(lr=learning_rate)
        elif optimizer == "RMSprop":
            return RMSprop(lr=learning_rate)
        elif optimizer == "Adadelta":
            return Adadelta(lr=learning_rate)
        elif optimizer == "Adagrad":
            return Adagrad(lr=learning_rate)
        elif optimizer == "SGD":
            return SGD(lr=learning_rate, momentum=0.9, nesterov=True)
        else:
            return Adam(lr=learning_rate)

    def get_convolution_hyperparameter(self, conv_layer, hp_list, hp_type):

        if "min" in self.hyperparameters[f"{hp_type}_{conv_layer}"]:
            min_value = self.hyperparameters[f"{hp_type}_{conv_layer}"]["min"]
        else:
            min_value = 1
        if "max" in self.hyperparameters[f"{hp_type}_{conv_layer}"]:
            max_value = self.hyperparameters[f"{hp_type}_{conv_layer}"]["max"]
        else:
            max_value = 4
        if "step" in self.hyperparameters[f"{hp_type}_{conv_layer}"]:
            step = self.hyperparameters[f"{hp_type}_{conv_layer}"]["step"]
        else:
            step = 8

        label = f"{hp_type}_{conv_layer}"

        if conv_layer > 1:
            if self.hyperparameters[label] == "equal_from_previous_convolution":
                new_hp = hp_list[conv_layer - 2]
            elif self.hyperparameters[label] == "double_from_previous_convolution":
                new_hp = hp_list[conv_layer - 2] * 2
            elif self.hyperparameters[label] == "half_from_previous_convolution":
                new_hp = int(hp_list[conv_layer - 2] / 2) if hp_list[conv_layer - 2] > 1 else 1
            else:
                if self.hyperparameters[label]["min"] == f"previous_convolution_{hp_type}":
                    new_hp = random.randrange(hp_list[conv_layer - 2], max_value + step, step)
                elif self.hyperparameters[label]["max"] == f"previous_convolution_{hp_type}":
                    new_hp = random.randrange(min_value, hp_list[conv_layer - 2] + step, step)
                else:
                    new_hp = random.randrange(min_value, max_value + step, step)
        else:
            new_hp = random.randrange(min_value, max_value + step, step)
        hp_list.append(new_hp)
        return hp_list

    def get_pooling_hyperparameter(self, conv_layer, hp_list, hp_type):

        if "min" in self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]:
            min_value = self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]["min"]
        else:
            min_value = 1
        if "max" in self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]:
            max_value = self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]["max"]
        else:
            max_value = 2
        if "step" in self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]:
            step = self.hyperparameters[f"pooling_{hp_type}_{conv_layer}"]["step"]
        else:
            step = 1
        label = f"pooling_{hp_type}_{conv_layer}"

        if conv_layer > 1:
            if self.hyperparameters[label] == "equal_from_previous_pooling":
                value = hp_list[conv_layer - 2]
            elif self.hyperparameters[label] == "double_from_previous_pooling":
                value = hp_list[conv_layer - 2] * 2
            elif self.hyperparameters[label] == "half_from_previous_pooling":
                value = int(hp_list[conv_layer - 2] / 2) if hp_list[conv_layer - 2] > 1 else 1
            else:
                if self.hyperparameters[label]["min"] == f"previous_pooling_{hp_type}":
                    value = random.randrange(hp_list[conv_layer - 2], max_value + step, step)
                elif self.hyperparameters[label]["max"] == f"previous_pooling_{hp_type}":
                    value = random.randrange(min_value, hp_list[conv_layer - 2] + step, step)
                else:
                    value = random.randrange(min_value, max_value + step, step)
        else:
            value = random.randrange(min_value, max_value + step, step)
        hp_list.append(value)
        return hp_list

    def get_pooling_type(self, conv_layer, hp_list):
        if conv_layer > 1:
            if self.hyperparameters[f"pooling_type_{conv_layer}"] == "equal_from_previous_pooling":
                hp_list.append(hp_list[conv_layer - 2])
            else:
                hp_list.append(random.choice(self.hyperparameters[f"pooling_type_{conv_layer}"]))
        else:
            hp_list.append(random.choice(self.hyperparameters[f"pooling_type_{conv_layer}"]))
        return hp_list
