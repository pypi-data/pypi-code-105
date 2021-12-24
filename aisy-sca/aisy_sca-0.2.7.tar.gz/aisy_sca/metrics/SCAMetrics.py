import numpy as np
import scipy.special as scipy_special


class SCAMetrics:

    def __init__(self, model, x_data, settings, label_key_guess):
        self.model = model
        self.x_data = x_data
        self.settings = settings
        self.label_key_guess = label_key_guess

    def run(self, random_states=None):

        nt = len(self.x_data)
        nt_interval = int(self.settings["key_rank_attack_traces"] / self.settings["key_rank_report_interval"])
        key_ranking_sum = np.zeros(nt_interval)
        success_rate_sum = np.zeros(nt_interval)
        r_states = []

        # ---------------------------------------------------------------------------------------------------------#
        # predict output probabilities for shuffled test or validation set
        # ---------------------------------------------------------------------------------------------------------#
        output_probabilities = self.model.predict(self.x_data)
        if self.model.layers[len(self.model.layers) - 1].get_config()['activation'] is not "softmax":
            output_probabilities = scipy_special.softmax(output_probabilities, axis=1)

        nb_guesses = len(self.label_key_guess)
        probabilities_kg_all_traces = np.zeros((nt, nb_guesses))
        for index in range(nt):
            probabilities_kg_all_traces[index] = output_probabilities[index][
                np.asarray([int(leakage[index]) for leakage in self.label_key_guess[:]])  # array with 256 leakage values (1 per key guess)
            ]

        for run in range(self.settings["key_rank_executions"]):

            if random_states is None:
                r_state = np.random.randint(1048576)
                np.random.seed(r_state)
                r = np.random.choice(nt, self.settings["key_rank_attack_traces"], replace=False)
            else:
                r_state = random_states[f"{run}"]
                np.random.seed(r_state)
                r = np.random.choice(nt, self.settings["key_rank_attack_traces"], replace=False)
            r_states.append(r_state)

            probabilities_kg_all_traces_shuffled = probabilities_kg_all_traces[r]

            key_probabilities = np.zeros(nb_guesses)

            kr_count = 0
            for index in range(self.settings["key_rank_attack_traces"]):

                key_probabilities += np.log(probabilities_kg_all_traces_shuffled[index] + 1e-36)
                key_probabilities_sorted = np.argsort(key_probabilities)[::-1]

                if (index + 1) % self.settings["key_rank_report_interval"] == 0:
                    key_ranking_good_key = list(key_probabilities_sorted).index(self.settings["good_key"]) + 1
                    key_ranking_sum[kr_count] += key_ranking_good_key

                    if key_ranking_good_key == 1:
                        success_rate_sum[kr_count] += 1

                    kr_count += 1

        guessing_entropy = key_ranking_sum / self.settings["key_rank_executions"]
        success_rate = success_rate_sum / self.settings["key_rank_executions"]
        if guessing_entropy[nt_interval - 1] < 2:
            result_number_of_traces_ge_1 = self.settings["key_rank_attack_traces"] - np.argmax(guessing_entropy[::-1] > 2) * self.settings[
                "key_rank_report_interval"]
        else:
            result_number_of_traces_ge_1 = self.settings["key_rank_executions"]

        print(f"GE = {guessing_entropy[nt_interval - 1]}")
        print(f"SR = {success_rate[nt_interval - 1]}")
        if guessing_entropy[nt_interval - 1] < 2:
            print(f"Number of traces to reach GE = 1: {result_number_of_traces_ge_1}")

        return guessing_entropy, success_rate, result_number_of_traces_ge_1, output_probabilities, r_states
