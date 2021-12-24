from aisy_sca.analysis.SingleModel import SingleModel
from aisy_sca.analysis.MultiModel import MultiModel
from aisy_sca.AnalysisDatabaseControls import *
from aisy_sca.LeakageModelControls import *


class SingleProcess:

    def __init__(self, dataset, settings, models, da_function, labels_key_guesses_attack_set=None, labels_key_guesses_validation_set=None,
                 random_states=None):
        self.dataset = dataset
        self.settings = settings
        self.models = models
        self.da_function = da_function
        self.custom_callbacks = None
        self.labels_key_guesses_attack_set = labels_key_guesses_attack_set
        self.labels_key_guesses_validation_set = labels_key_guesses_validation_set
        self.random_states = random_states

    def run(self):

        """ Create analysis in database """
        analysis_db_controls = AnalysisDatabaseControls(self.settings)
        self.settings["analysis_id"] = analysis_db_controls.analysis_id
        analysis_db_controls.save_leakage_model_to_database()

        """ Generate list of labels for all key guesses for validation and attack sets """
        if self.labels_key_guesses_attack_set is None and self.labels_key_guesses_validation_set is None:
            lm_control = LeakageModelControls(self.settings)
            self.labels_key_guesses_attack_set, self.labels_key_guesses_validation_set = lm_control.compute_labels_key_guesses(self.dataset)

        """ If number of neural networks is larger than 1, starts multi-model process. Otherwise, runs single-model process """
        if len(self.models) > 1:
            multi_model = MultiModel(self.settings, self.dataset, self.da_function, random_states=self.random_states)
            multi_model.labels_key_guesses_attack_set = self.labels_key_guesses_attack_set
            multi_model.labels_key_guesses_validation_set = self.labels_key_guesses_validation_set
            multi_model.analysis_db_controls = analysis_db_controls
            multi_model.run(self.models)
            self.custom_callbacks = multi_model.custom_callbacks
        else:
            single_model = SingleModel(self.settings, self.dataset, self.da_function, random_states=self.random_states)
            single_model.labels_key_guesses_attack_set = self.labels_key_guesses_attack_set
            single_model.labels_key_guesses_validation_set = self.labels_key_guesses_validation_set
            single_model.analysis_db_controls = analysis_db_controls
            single_model.run(self.models["0"])
            self.custom_callbacks = single_model.custom_callbacks
