import tensorflow.keras.backend as backend
import numpy as np
import json
import time
import os


class Utils:

    def keras_model_as_string(self, model, model_name):
        model_json = json.loads(model.to_json())

        file_contents = f"def {model_name}(classes, number_of_samples):\n"
        for index, layers in enumerate(model_json["config"]["layers"]):
            if index == 0:
                file_contents += "    model = Sequential(name='{}')\n".format(model_json["config"]["name"])
            if "Conv" in layers["class_name"]:
                input_layer = ", input_shape=({}, 1)".format(layers["config"]["batch_input_shape"][1]) if "batch_input_shape" in layers[
                    "config"] else ""
                file_contents += "    model.add(Conv1D(filters={}, kernel_size={}, strides={}, activation='{}', padding='{}', " \
                                 "kernel_initializer='{}', bias_initializer='{}'{}))\n".format(
                    layers["config"]["filters"], layers["config"]["kernel_size"], layers["config"]["strides"],
                    layers["config"]["activation"], layers["config"]["padding"], layers["config"]["kernel_initializer"]["class_name"],
                    layers["config"]["bias_initializer"]["class_name"], input_layer)
            elif "AveragePooling" in layers["class_name"]:
                file_contents += "    model.add(AveragePooling1D(pool_size={}, strides={}))\n".format(layers["config"]["pool_size"],
                                                                                                      layers["config"]["strides"])
            elif "MaxPool" in layers["class_name"]:
                file_contents += "    model.add(MaxPool1D(pool_size={}, strides={}))\n".format(layers["config"]["pool_size"],
                                                                                               layers["config"]["strides"])
            elif "Norm" in layers["class_name"]:
                file_contents += "    model.add(BatchNormalization())\n"
            elif "Flatten" in layers["class_name"]:
                file_contents += "    model.add(Flatten())\n"
            elif "ActivityRegularization" in layers["class_name"]:
                file_contents += "    model.add(ActivityRegularization(l1={}, l2={}))\n".format(layers["config"]["l1"],
                                                                                                layers["config"]["l2"])
            elif "Activation" in layers["class_name"]:
                file_contents += "    model.add(Activation(activation={})\n".format(layers["config"]["activation"])
            elif "Dropout" in layers["class_name"]:
                file_contents += "    model.add(Dropout({}))\n".format(layers["config"]["rate"])
            elif "Dense" in layers["class_name"]:
                input_layer = ", input_shape=({},)".format(layers["config"]["batch_input_shape"][1]) if "batch_input_shape" in layers[
                    "config"] else ""
                file_contents += "    model.add(Dense({}, activation='{}', kernel_initializer='{}', bias_initializer='{}'{}))\n".format(
                    layers["config"]["units"], layers["config"]["activation"], layers["config"]["kernel_initializer"]["class_name"],
                    layers["config"]["bias_initializer"]["class_name"], input_layer)
        file_contents += "    model.summary()\n"
        file_contents += "    optimizer = {}(lr={})\n".format(model.optimizer.__class__.__name__, backend.eval(model.optimizer.lr), 2)
        metric_names = []
        for metric in model.metrics_names:
            if "loss" not in metric:
                metric_names.append(metric)
        file_contents += "    model.compile(loss='{}', optimizer=optimizer, metrics={})\n".format(model.loss, metric_names)
        file_contents += "    return model"
        return file_contents

    def get_hyperparameters_from_model(self, model):
        model_json = json.loads(model.to_json())

        conv_layers = 0
        kernels = []
        strides = []
        filters = []
        pooling_types = []
        pooling_sizes = []
        pooling_strides = []
        neurons = 0
        dense_layers = 0
        activation = "relu"
        learning_rate = float(backend.eval(model.optimizer.lr))
        optimizer = str(model.optimizer.__class__.__name__)
        dropout_rate = 0
        layers_structure = []

        for index, layers in enumerate(model_json["config"]["layers"]):
            layers_structure.append(layers["class_name"])
            if "Conv" in layers["class_name"]:
                conv_layers += 1
                filters.append(int(layers["config"]["filters"]))
                strides.append(int(layers["config"]["strides"][0]))
                kernels.append(int(layers["config"]["kernel_size"][0]))
                activation = str(layers["config"]["activation"])
            elif "AveragePooling" in layers["class_name"]:
                pooling_types.append("Average")
                pooling_sizes.append(int(layers["config"]["pool_size"][0]))
                pooling_strides.append(int(layers["config"]["strides"][0]))
            elif "MaxPool" in layers["class_name"]:
                pooling_types.append("Max")
                pooling_sizes.append(int(layers["config"]["pool_size"][0]))
                pooling_strides.append(int(layers["config"]["strides"][0]))
            elif "Dropout" in layers["class_name"]:
                dropout_rate = layers["config"]["rate"]
            elif "Dense" in layers["class_name"]:
                if index < len(model_json["config"]["layers"]) - 1:
                    dense_layers += 1
                    neurons = int(layers["config"]["units"])
                    activation = str(layers["config"]["activation"])

        hp_list = {
            "neurons": neurons,
            "layers": dense_layers,
            "activation": activation,
            "learning_rate": float(learning_rate),
            "dropout_rate": dropout_rate,
            "optimizer": optimizer,
            "layers_structure": layers_structure
        }
        if conv_layers > 0:
            hp_list["conv_layers"] = conv_layers
            hp_list["kernels"] = kernels
            hp_list["strides"] = strides
            hp_list["filters"] = filters
            hp_list["pooling_types"] = pooling_types
            hp_list["pooling_sizes"] = pooling_sizes
            hp_list["pooling_strides"] = pooling_strides
        hp_list["parameters"] = model.count_params()

        return hp_list

    def adapt_folder_path(self, path):
        if "/" in path and path[len(path) - 1] != "/":
            path += "/"
        if "\\" in path and path[len(path) - 1] != "\\":
            path += "\\"
        return path

    def get_variable_name(self, var):
        return [tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())]
