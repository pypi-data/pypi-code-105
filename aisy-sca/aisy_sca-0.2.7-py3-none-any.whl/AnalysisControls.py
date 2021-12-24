import os


class AnalysisControls:

    def __init__(self, settings, models):
        self.settings = settings
        self.models = models

    def update_settings(self, random_search, grid_search, visualization, early_stopping, data_augmentation, callbacks, ensemble,
                        confusion_matrix, profiling_analyzer):

        self.settings["grid_search"] = grid_search
        self.settings["random_search"] = random_search
        self.settings["ensemble"] = ensemble
        self.settings["early_stopping"] = early_stopping
        self.settings["custom_callbacks"] = callbacks
        self.settings["confusion_matrix"] = confusion_matrix
        self.settings["use_grid_search"] = True if grid_search is not None else False
        self.settings["use_random_search"] = True if random_search is not None else False
        self.settings["use_profiling_analyzer"] = True if profiling_analyzer is not None else False

        if visualization is not None:
            self.settings["use_visualization"] = True
            self.settings["visualization"] = visualization[0]
        else:
            self.settings["use_visualization"] = False

        if data_augmentation is not None:
            self.settings["use_data_augmentation"] = True
            self.settings["data_augmentation"] = [data_augmentation[0].__name__, data_augmentation[1]]
        else:
            self.settings["use_data_augmentation"] = False

        if callbacks is not None:
            self.settings["use_custom_callbacks"] = True
        else:
            self.settings["use_custom_callbacks"] = False

        if early_stopping is not None:
            self.settings["use_early_stopping"] = True
            self.settings["early_stopping"] = early_stopping
        else:
            self.settings["use_early_stopping"] = False

        self.settings["use_ensemble"] = True if ensemble is not None else False
        self.settings["use_confusion_matrix"] = confusion_matrix
        self.settings["split_test_set"] = self.settings["use_ensemble"] or self.settings["use_early_stopping"] or self.settings[
            "use_grid_search"] or self.settings["use_random_search"]
        self.settings["split_training_set"] = False

        if self.settings["use_grid_search"] or self.settings["use_random_search"]:
            self.settings["hyperparameter_search"] = True
        else:
            self.settings["hyperparameter_search"] = False

        """ set default value """
        self.settings["profiling_analyzer_steps"] = [self.settings["number_of_profiling_traces"]]

        """ or set the list of steps in case profiling analyzer is considered"""
        if self.settings["use_profiling_analyzer"]:
            if isinstance(profiling_analyzer["steps"], list):
                self.settings["profiling_analyzer_steps"] = profiling_analyzer["steps"]
            else:
                self.settings["profiling_analyzer_steps"] = []
                for step in range(profiling_analyzer["steps"]):
                    n_profiling_traces = int(self.settings["number_of_profiling_traces"] / profiling_analyzer["steps"])
                    n_profiling_traces = n_profiling_traces * (step + 1)
                    self.settings["profiling_analyzer_steps"].append(n_profiling_traces)

    def check_errors(self):

        if self.settings["database_root_folder"] is None:
            print("ERROR: database root folder not defined. Use method 'set_database_root_folder' to define your database root folder.")
            return

        if self.settings["datasets_root_folder"] is None:
            print("ERROR: dataset root folder not defined. Use method 'set_dataset_root_folder' to define your dataset root folder.")
            return

        if self.settings["resources_root_folder"] is None:
            print("ERROR: resources root folder not defined. Use method 'set_resources_root_folder' to define your resources root folder.")
            return

        for folder in ["databases", "figures", "models", "npz"]:
            dir_resources_id = "{}/{}/".format(self.settings["resources_root_folder"], folder)
            if not os.path.exists(dir_resources_id):
                os.makedirs(dir_resources_id)

        if len(self.models) == 0 and self.settings["grid_search"] is None and self.settings["random_search"] is None:
            print("ERROR 1: neural network model is not defined.")
            return

        if "filename" not in self.settings.keys():
            print("ERROR 2: Dataset 'filename' not specified. Please use set_filename method to specify it.")
            return

        if "key" not in self.settings.keys():
            print("ERROR 3: Dataset 'key' not specified. Please use set_key method to specify it.")
            return

        if "first_sample" not in self.settings.keys():
            print("ERROR 4 : Dataset 'first_sample' not specified. Please use set_first_sample method to specify it.")
            return

        if "number_of_samples" not in self.settings.keys():
            print("ERROR 5: Dataset 'number_of_samples' not specified. Please use set_number_of_samples method to specify it.")
            return

        if "number_of_profiling_traces" not in self.settings.keys():
            print(
                "ERROR 6: Dataset 'number_of_profiling_traces' not specified. Please use set_number_of_profiling_traces method to specify it.")
            return

        if "number_of_attack_traces" not in self.settings.keys():
            print("ERROR 7: Dataset 'number_of_attack_traces' not specified. Please use set_number_of_attack_traces method to specify it.")
            return

        if self.settings["use_ensemble"]:
            if self.settings["number_of_attack_traces"] == self.settings["key_rank_attack_traces"]:
                print("ERROR 8: ensemble feature requires the 'number_of_attack_traces' >= 2 x key_rank_attack_traces.")
                return

        if self.settings["use_grid_search"]:
            if self.settings["use_ensemble"] and self.settings["grid_search"]["stop_condition"]:
                print("ERROR 11: when grid search has a stop condition, ensembles can't be applied.")
                return
            if self.settings["number_of_attack_traces"] == self.settings["key_rank_attack_traces"]:
                print("ERROR 14: grid search feature requires the 'number_of_attack_traces' >= 2 x key_rank_attack_traces.")
                return

        if self.settings["use_random_search"]:
            if self.settings["use_ensemble"]:
                if self.settings["ensemble"][0] > self.settings["random_search"]["max_trials"]:
                    print("ERROR 12: number of models for ensembles can't be larger than maximum number of trials in random search.")
                    return
            if self.settings["use_ensemble"] and self.settings["random_search"]["stop_condition"]:
                print("ERROR 13: when random search has a stop condition, ensembles can't be applied.")
                return
            if self.settings["number_of_attack_traces"] == self.settings["key_rank_attack_traces"]:
                print("ERROR 15: random search feature requires the 'number_of_attack_traces' >= 2 x key_rank_attack_traces.")
                return

        if self.settings["use_early_stopping"]:
            if self.settings["number_of_attack_traces"] == self.settings["key_rank_attack_traces"]:
                print("ERROR 9: early stopping feature requires the 'number_of_attack_traces' >= 2 x key_rank_attack_traces.")
                return
