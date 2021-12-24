from aisy_sca.analysis.SingleModel import SingleModel
import time


class MultiModel:

    def __init__(self, settings, dataset, da_function, random_states=None):
        self.settings = settings
        self.dataset = dataset
        self.labels_key_guesses_attack_set = None
        self.labels_key_guesses_validation_set = None
        self.analysis_db_controls = None
        self.da_function = da_function
        self.custom_callbacks = []
        self.random_states = random_states

    def run(self, models):
        start = time.time()

        for model_index, model in models.items():
            single_model = SingleModel(self.settings, self.dataset, self.da_function, random_states=self.random_states)
            single_model.labels_key_guesses_attack_set = self.labels_key_guesses_attack_set
            single_model.labels_key_guesses_validation_set = self.labels_key_guesses_validation_set
            single_model.analysis_db_controls = self.analysis_db_controls
            single_model.run(model)
            self.custom_callbacks.append(single_model.get_custom_callbacks())

        self.analysis_db_controls.update_results_in_database(time.time() - start)
