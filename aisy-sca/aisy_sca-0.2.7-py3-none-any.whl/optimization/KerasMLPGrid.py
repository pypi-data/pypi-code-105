from tensorflow.keras.optimizers import *
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow as tf
import numpy as np
import importlib


class KerasMLPGrid:

    def __init__(self, settings, hyperparameters, fixed_model=False, loss_function=None):
        self.settings = settings
        self.hyperparameters = hyperparameters
        self.model_structure = settings["grid_search"]["structure"]
        self.fixed_model = fixed_model
        self.loss_function = loss_function

    def mlp_grid_search(self):

        neurons = self.hyperparameters["neurons"] if "neurons" in self.hyperparameters else 50
        layers = self.hyperparameters["layers"] if "layers" in self.hyperparameters else 5
        activation = self.hyperparameters["activation"] if "activation" in self.hyperparameters else "relu"
        learning_rate = self.hyperparameters["learning_rate"] if "learning_rate" in self.hyperparameters else 0.001
        optimizer = self.hyperparameters["optimizer"] if "optimizer" in self.hyperparameters else "Adam"
        dropout_rate = self.hyperparameters["dropout_rate"] if "dropout_rate" in self.hyperparameters else 0
        random_seed = self.hyperparameters["seed"] if self.fixed_model else np.random.randint(1048576)

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
            if "pooling_size_0" in self.hyperparameters and "pooling_stride_0" in self.hyperparameters and "pooling_type_0" in self.hyperparameters:
                pooling_sizes_0 = self.hyperparameters["pooling_size_0"]
                pooling_stride_0 = self.hyperparameters["pooling_stride_0"]
                pooling_type_0 = self.hyperparameters["pooling_type_0"]
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
