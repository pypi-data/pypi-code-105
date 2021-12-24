from aisy_database.db_update import DBUpdate
from aisy_database.db_save import DBSave
from aisy_database.db_select import DBSelect
from aisy_database.db_tables import *


class AnalysisDatabaseControls:

    def __init__(self, settings):
        self.settings = settings
        self.db_save = DBSave(f"{settings['database_root_folder']}{settings['database_name']}")
        self.analysis_id = self.db_save.db_save_analysis(settings['database_name'], settings["filename"], settings)
        self.db_save.analysis_id = self.analysis_id
        self.db_update = DBUpdate(f"{settings['database_root_folder']}{settings['database_name']}", self.analysis_id)
        self.db_select = DBSelect(f"{settings['database_root_folder']}{settings['database_name']}")

    def update_results_in_database(self, elapsed_time):
        self.db_update.db_update_settings(self.settings)
        self.db_update.db_update_elapsed_time(elapsed_time)

    def save_leakage_model_to_database(self):
        if "leakage_model" in self.settings:
            leakage_model = {
                "cipher": self.settings["leakage_model"]["cipher"],
                "leakage_model": self.settings["leakage_model"]["leakage_model"],
                "byte": self.settings["leakage_model"]["byte"],
                "round": self.settings["leakage_model"]["round"],
                "target_state": self.settings["leakage_model"]["target_state"],
                "direction": self.settings["leakage_model"]["direction"],
                "attack_direction": self.settings["leakage_model"]["attack_direction"]
            }
            if self.settings["leakage_model"]["leakage_model"] == "bit":
                leakage_model["bit"] = self.settings["leakage_model"]["bit"]

            if self.settings["leakage_model"]["leakage_model"] == "HD":
                leakage_model["round_first"] = self.settings["leakage_model"]["round_first"]
                leakage_model["round_second"] = self.settings["leakage_model"]["round_second"]
                leakage_model["target_state_first"] = self.settings["leakage_model"]["target_state_first"]
                leakage_model["target_state_second"] = self.settings["leakage_model"]["target_state_second"]
        else:
            leakage_model = {"leakage_model": "Unknown", "cipher": "Unknown", "byte": "Unknown"}

        self.db_save.db_save_leakage_model(leakage_model)

    def save_visualization_results_to_database(self, input_gradients_epochs, input_gradients_sum, hp_id):
        self.db_save.db_save_visualization(input_gradients_epochs, input_gradients_sum, f"Input Gradients {hp_id}", hp_id)

    def save_confusion_matrix_results_to_database(self, confusion_matrix, hp_id):
        self.db_save.db_save_confusion_matrix(confusion_matrix, hp_id)

    def save_sca_metrics_to_database(self, ge, sr, db_metric_name, hp_id, r, index):
        metric_id = self.db_save.db_save_key_rank(ge, db_metric_name, self.settings["key_rank_report_interval"])
        self.db_save.db_save_guessing_entropy_hyperparameter(metric_id, hp_id)
        metric_id = self.db_save.db_save_success_rate(sr, db_metric_name, self.settings["key_rank_report_interval"])
        self.db_save.db_save_success_rate_hyperparameter(metric_id, hp_id)
        self.db_save.db_save_random_state_hyperparameter(db_metric_name, index, r)

    def save_model_description_to_database(self, model_description, model_name, hyperparameters_id):
        self.db_save.db_save_neural_network(model_description, model_name, hyperparameters_id)

    def save_hyper_parameters_to_database(self, hyper_parameters_list):
        return self.db_save.db_save_hyper_parameters(hyper_parameters_list)

    def update_hyper_parameters_to_database(self, hyper_parameters_list, hp_id):
        self.db_update.db_update_hyperparameters(hyper_parameters_list, hp_id, "hyperparameters")

    def update_guessing_entropy_label(self, old_label, new_label):
        self.db_update.db_update_key_rank_label(old_label, new_label)

    def update_success_rate_label(self, old_label, new_label):
        self.db_update.db_update_success_rate_label(old_label, new_label)

    def update_metric_label(self, old_label, new_label):
        self.db_update.db_update_metric_label(old_label, new_label)

    def update_random_state_label(self, old_label, new_label):
        self.db_update.db_update_random_state_label(old_label, new_label)

    def save_generic_metrics(self, history, early_stopping_metrics, early_stopping_epoch_values, hp_id, search_index=None,
                             n_profiling_traces=None):
        if self.settings["use_profiling_analyzer"]:
            metric_id = self.db_save.db_save_metric(history.history["loss"],
                                                    f"loss {n_profiling_traces} traces" if search_index is None else f"loss {search_index} {n_profiling_traces} traces")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["accuracy"],
                                                    f"accuracy {n_profiling_traces} traces" if search_index is None else f"accuracy {search_index} {n_profiling_traces} traces")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["val_loss"],
                                                    f"val_loss {n_profiling_traces} traces" if search_index is None else f"val_loss {search_index} {n_profiling_traces} traces")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["val_accuracy"],
                                                    f"val_accuracy {n_profiling_traces} traces" if search_index is None else f"val_accuracy {search_index} {n_profiling_traces} traces")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            if early_stopping_metrics is not None and early_stopping_epoch_values is not None:
                for es_metric in early_stopping_metrics:
                    metric_id = self.db_save.db_save_metric(early_stopping_epoch_values[es_metric],
                                                            f"val_{es_metric} {n_profiling_traces} traces" if search_index is None else f"val_{es_metric} {search_index} {n_profiling_traces} traces")
                    self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
        else:
            metric_id = self.db_save.db_save_metric(history.history["loss"], "loss" if search_index is None else f"loss {search_index}")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["accuracy"],
                                                    "accuracy" if search_index is None else f"accuracy {search_index}")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["val_loss"],
                                                    "val_loss" if search_index is None else f"val_loss {search_index}")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            metric_id = self.db_save.db_save_metric(history.history["val_accuracy"],
                                                    "val_accuracy" if search_index is None else f"val_accuracy {search_index}")
            self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)
            if early_stopping_metrics is not None and early_stopping_epoch_values is not None:
                for es_metric in early_stopping_metrics:
                    metric_id = self.db_save.db_save_metric(early_stopping_epoch_values[es_metric],
                                                            f"val_{es_metric}" if search_index is None else f"val_{es_metric} {search_index}")
                    self.db_save.db_save_metric_hyperparameter(metric_id, hp_id)

    def update_best_model_metrics(self, best_model_index, early_stopping_metrics, steps=None):

        """ Update label of best Guessing Entropy and Success Rate in database """

        if self.settings["use_profiling_analyzer"]:
            for n in steps:
                self.update_guessing_entropy_label(f"Attack Set {best_model_index[f'{n}']} {n} traces",
                                                   f"Attack Set Best Model {n} traces")
                self.update_guessing_entropy_label(f"Validation Set {best_model_index[f'{n}']} {n} traces",
                                                   f"Validation Set Best Model {n} traces")
                self.update_success_rate_label(f"Attack Set {best_model_index[f'{n}']} {n} traces",
                                               f"Attack Set Best Model {n} traces")
                self.update_success_rate_label(f"Validation Set {best_model_index[f'{n}']} {n} traces",
                                               f"Validation Set Best Model {n} traces")
                self.update_metric_label(f"accuracy {best_model_index[f'{n}']} {n} traces",
                                         f"accuracy Best Model {n} traces")
                self.update_metric_label(f"loss {best_model_index[f'{n}']} {n} traces",
                                         f"loss Best Model {n} traces")
                self.update_metric_label(f"val_accuracy {best_model_index[f'{n}']} {n} traces",
                                         f"val_accuracy Best Model {n} traces")
                self.update_metric_label(f"val_loss {best_model_index[f'{n}']} {n} traces",
                                         f"val_loss Best Model {n} traces")
                if early_stopping_metrics is not None:
                    for es_metric in early_stopping_metrics:
                        self.update_guessing_entropy_label(f"ES Attack Set {es_metric} {best_model_index[f'{n}']} {n} traces",
                                                           f"ES Attack Set {es_metric} Best Model {n} traces")
                        self.update_guessing_entropy_label(f"ES Validation Set {es_metric} {best_model_index[f'{n}']} {n} traces",
                                                           f"ES Validation Set {es_metric} Best Model {n} traces")
                        self.update_success_rate_label(f"ES Attack Set {es_metric} {best_model_index[f'{n}']} {n} traces",
                                                       f"ES Attack Set {es_metric} Best Model {n} traces")
                        self.update_success_rate_label(f"ES Validation Set {es_metric} {best_model_index[f'{n}']} {n} traces",
                                                       f"ES Validation Set {es_metric} Best Model {n} traces")
                        self.update_metric_label(f"val_{es_metric} {best_model_index[f'{n}']} {n} traces",
                                                 f"val_{es_metric} Best Model {n} traces")
        else:
            self.update_guessing_entropy_label(f"Attack Set {best_model_index}", "Attack Set Best Model")
            self.update_guessing_entropy_label(f"Validation Set {best_model_index}", "Validation Set Best Model")
            self.update_success_rate_label(f"Attack Set {best_model_index}", "Attack Set Best Model")
            self.update_success_rate_label(f"Validation Set {best_model_index}", "Validation Set Best Model")
            self.update_metric_label(f"accuracy {best_model_index}", "accuracy Best Model")
            self.update_metric_label(f"loss {best_model_index}", "loss Best Model")
            self.update_metric_label(f"val_accuracy {best_model_index}", "val_accuracy Best Model")
            self.update_metric_label(f"val_loss {best_model_index}", "val_loss Best Model")
            if early_stopping_metrics is not None:
                for es_metric in early_stopping_metrics:
                    self.update_guessing_entropy_label(f"ES Attack Set {es_metric} {best_model_index}",
                                                       f"ES Attack Set {es_metric} Best Model")
                    self.update_guessing_entropy_label(f"ES Validation Set {es_metric} {best_model_index}",
                                                       f"ES Validation Set {es_metric} Best Model")
                    self.update_success_rate_label(f"ES Attack Set {es_metric} {best_model_index}",
                                                   f"ES Attack Set {es_metric} Best Model")
                    self.update_success_rate_label(f"ES Validation Set {es_metric} {best_model_index}",
                                                   f"ES Validation Set {es_metric} Best Model")
                    self.update_metric_label(f"val_{es_metric} {best_model_index}", f"val_{es_metric} Best Model")

    def select_all_guessing_entropy_from_analysis(self, n_profiling=None):
        ge_values = self.db_select.select_all_guessing_entropy_from_analysis(GuessingEntropy, self.settings["analysis_id"])

        ge_validation = []
        ge_attack = []

        for ge in ge_values:
            self.append_result(ge_validation, ge, "Validation", n_profiling)
            self.append_result(ge_attack, ge, "Attack", n_profiling)

        return ge_validation, ge_attack

    def select_all_success_rate_from_analysis(self, n_profiling=None):
        sr_values = self.db_select.select_all_success_rate_from_analysis(SuccessRate, self.settings["analysis_id"])

        sr_validation = []
        sr_attack = []
        for sr in sr_values:
            self.append_result(sr_validation, sr, "Validation", n_profiling)
            self.append_result(sr_attack, sr, "Attack", n_profiling)

        return sr_validation, sr_attack

    def select_all_early_stopping_guessing_entropy_from_analysis(self, early_stopping_metric, n_profiling=None):
        ge_values = self.db_select.select_all_guessing_entropy_from_analysis(GuessingEntropy, self.settings["analysis_id"])

        ge_validation = []
        ge_attack = []
        for ge in ge_values:
            self.append_result_early_stopping(ge_validation, ge, "Validation", n_profiling, early_stopping_metric)
            self.append_result_early_stopping(ge_attack, ge, "Attack", n_profiling, early_stopping_metric)

        return ge_validation, ge_attack

    def select_all_early_stopping_success_rate_from_analysis(self, early_stopping_metric, n_profiling=None):
        sr_values = self.db_select.select_all_success_rate_from_analysis(SuccessRate, self.settings["analysis_id"])

        sr_validation = []
        sr_attack = []
        for sr in sr_values:
            self.append_result_early_stopping(sr_validation, sr, "Validation", n_profiling, early_stopping_metric)
            self.append_result_early_stopping(sr_attack, sr, "Attack", n_profiling, early_stopping_metric)

        return sr_validation, sr_attack

    def append_result(self, result_list, result, label_set, n_profiling):
        if label_set in result["label"] and "ES" not in result["label"]:
            if n_profiling is not None:
                if f"{n_profiling} traces" in result["label"]:
                    result_list.append(result["values"])
            else:
                result_list.append(result["values"])

    def append_result_early_stopping(self, result_list, result, label_set, n_profiling, early_stopping_metric):
        if label_set in result["label"] and "ES" in result["label"] and early_stopping_metric in result["label"]:
            if n_profiling is not None:
                if f"{n_profiling} traces" in result["label"]:
                    result_list.append(result["values"])
            else:
                result_list.append(result["values"])

    def save_ensemble_guessing_entropy_results(self, ge, label):
        self.db_save.db_save_key_rank(ge, label, self.settings["key_rank_report_interval"])

    def save_ensemble_success_rate_results(self, sr, label):
        self.db_save.db_save_success_rate(sr, label, self.settings["key_rank_report_interval"])
