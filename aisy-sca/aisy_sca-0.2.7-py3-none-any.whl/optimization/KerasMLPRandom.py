from tensorflow.keras.optimizers import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow as tf
import numpy as np
import random
import importlib


class KerasMLPRandom:

    def __init__(self, settings, hyperparameters, fixed_model=False, loss_function=None):
        self.settings = settings
        self.hyper_parameters = hyperparameters
        self.model_structure = settings["random_search"]["structure"]
        self.fixed_model = fixed_model
        self.loss_function = loss_function

    def mlp_random_search(self):
        if self.fixed_model:
            neurons = self.hyper_parameters["neurons"] if "neurons" in self.hyper_parameters else 50
            layers = self.hyper_parameters["layers"] if "layers" in self.hyper_parameters else 5
            activation = self.hyper_parameters["activation"] if "activation" in self.hyper_parameters else "relu"
            learning_rate = self.hyper_parameters["learning_rate"] if "learning_rate" in self.hyper_parameters else 0.001
            optimizer = self.hyper_parameters["optimizer"] if "optimizer" in self.hyper_parameters else "Adam"
            dropout_rate = self.hyper_parameters["dropout_rate"] if "dropout_rate" in self.hyper_parameters else 0
            random_seed = self.hyper_parameters["seed"] if "seed" in self.hyper_parameters else np.random.randint(1048576)
        else:
            # set default values if not present in hyper_parameters_ranges
            neurons = random.randrange(self.hyper_parameters["neurons"]["min"], self.hyper_parameters["neurons"]["max"] + self.hyper_parameters["neurons"]["step"],
                                       self.hyper_parameters["neurons"]["step"]) if "neurons" in self.hyper_parameters else 50
            layers = random.randrange(self.hyper_parameters["layers"]["min"], self.hyper_parameters["layers"]["max"] + self.hyper_parameters["layers"]["step"],
                                      self.hyper_parameters["layers"]["step"]) if "layers" in self.hyper_parameters else 5
            activation = random.choice(self.hyper_parameters["activation"]) if "activation" in self.hyper_parameters else "relu"
            learning_rate = random.choice(self.hyper_parameters["learning_rate"]) if "learning_rate" in self.hyper_parameters else 0.001
            optimizer = random.choice(self.hyper_parameters["optimizer"]) if "optimizer" in self.hyper_parameters else "Adam"
            if self.model_structure["use_dropout_after_dense_layer"] or self.model_structure["use_dropout_before_dense_layer"]:
                dropout_rate = random.choice(self.hyper_parameters["dropout_rate"])
            else:
                dropout_rate = 0
            random_seed = np.random.randint(1048576)

        hp = {
            'neurons': neurons,
            'layers': layers,
            'activation': activation,
            'learning_rate': learning_rate,
            'optimizer': optimizer,
            'seed': random_seed
        }

        if self.model_structure["use_dropout_after_dense_layer"] or self.model_structure["use_dropout_before_dense_layer"]:
            hp['dropout_rate'] = dropout_rate

        tf.random.set_seed(random_seed)

        model = Sequential()
        if self.model_structure["use_pooling_before_first_dense"]:
            if "pooling_size_0" in self.hyper_parameters and "pooling_stride_0" in self.hyper_parameters and "pooling_type_0" in self.hyper_parameters:
                pooling_sizes_0 = random.randrange(self.hyper_parameters["pooling_size_0"]["min"],
                                                   self.hyper_parameters["pooling_size_0"]["max"] + self.hyper_parameters["pooling_size_0"]["step"],
                                                   self.hyper_parameters["pooling_size_0"]["step"])
                pooling_stride_0 = random.randrange(self.hyper_parameters["pooling_stride_0"]["min"],
                                                    self.hyper_parameters["pooling_stride_0"]["max"] + self.hyper_parameters["pooling_stride_0"]["step"],
                                                    self.hyper_parameters["pooling_stride_0"]["step"])
                pooling_type_0 = random.choice(self.hyper_parameters["pooling_type_0"])
                if pooling_type_0 == "average":
                    model.add(AveragePooling1D(pool_size=pooling_sizes_0, strides=pooling_stride_0),
                              input_shape=(self.settings["number_of_samples"], 1))
                else:
                    model.add(MaxPool1D(pool_size=pooling_sizes_0, strides=pooling_stride_0,
                                        input_shape=(self.settings["number_of_samples"], 1)))
                model.add(Flatten())
                if self.model_structure["use_dropout_before_dense_layer"]:
                    model.add(Dropout(dropout_rate))
                model.add(Dense(neurons, activation=activation, input_shape=(self.settings["number_of_samples"],)))

                hp["pooling_size_0"] = pooling_sizes_0
                hp["pooling_stride_0"] = pooling_stride_0
                hp["pooling_type_0"] = pooling_type_0
        else:
            if self.model_structure["use_dropout_before_dense_layer"]:
                model.add(Dropout(dropout_rate))
            model.add(Dense(neurons, activation=activation, input_shape=(self.settings["number_of_samples"],)))
        if self.model_structure["use_dropout_after_dense_layer"]:
            model.add(Dropout(dropout_rate))
        for layer_index in range(layers - 1):
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
