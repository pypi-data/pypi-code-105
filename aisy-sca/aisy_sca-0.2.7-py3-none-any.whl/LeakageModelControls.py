from aisy_sca.crypto.sca_aes_create_intermediates import *
import numpy as np


class LeakageModelControls:

    def __init__(self, settings):
        self.settings = settings

    def set(self, leakage_model="HW", bit=0, byte=0, round=1, round_first=1, round_second=1, cipher="AES128",
            target_state="Sbox", target_state_first="Sbox", target_state_second="Sbox",
            direction="Encryption", attack_direction="input"):

        """
        Function to set the AES Leakage Model in the profiled SCA execution.
        :parameter
            leakage_model: 'HW', 'ID' or 'bit'
            bit: index of target bit (min 0, max 7)
            byte: index of target key byte
            round: index the target round
            round_first: index the first target round
            round_second: index the second target seround
            target_state: 'Sbox', InvSbox', 'AddRoundKey', 'MixColumns', 'InvMixColumns', 'ShiftRows', 'InvShiftRows'
            target_state_first: 'Input', 'Sbox', InvSbox', 'AddRoundKey', 'MixColumns', 'InvMixColumns', 'ShiftRows', 'InvShiftRows',
            'Output'
            target_state_second: 'Input', 'Sbox', InvSbox', 'AddRoundKey', 'MixColumns', 'InvMixColumns', 'ShiftRows', 'InvShiftRows',
            'Output'
            attack_direction: input, output
            direction: 'Encryption', 'Decryption'

        :return
            dictionary containing AES leakage model information:

            self.leakage_model = {
                "leakage_model": leakage_model,
                "bit": bit,
                "byte": byte,
                "round": round,
                "round_first": round_first,
                "round_second": round_second,
                "target_state": target_state,
                "target_state_first": target_state_first,
                "target_state_second": target_state_second,
                "direction": direction,
                "attack_direction": input
            }

        """

        self.settings["leakage_model"] = {
            "leakage_model": leakage_model,
            "bit": bit,
            "byte": byte,
            "round": round,
            "round_first": round_first,  # for Hamming Distance
            "round_second": round_second,  # for Hamming Distance
            "cipher": cipher,
            "target_state": target_state,
            "target_state_first": target_state_first,  # for Hamming Distance
            "target_state_second": target_state_second,  # for Hamming Distance
            "direction": direction,
            "attack_direction": attack_direction
        }

        if self.settings is not None:
            if self.settings["leakage_model"]["leakage_model"] == "HW" or self.settings["leakage_model"]["leakage_model"] == "HD":
                self.settings["classes"] = 9
            elif self.settings["leakage_model"]["leakage_model"] == "ID":
                self.settings["classes"] = 256
            else:
                self.settings["classes"] = 2
        else:
            print("Parameters (param) from target is not selected. Set target before the leakage model.")

        self.settings["leakage_model_is_set"] = True

        return self.settings

    def compute_labels_key_guesses(self, dataset):

        """ Function to compute all intermediate (labels) for all possible key guesses for AES """

        labels_key_guesses_attack_set = np.zeros((256, len(dataset.x_attack)), dtype="int64")
        for key_byte_hypothesis in range(256):
            key_h = bytearray.fromhex(self.settings["key"])
            key_h[self.settings["leakage_model"]["byte"]] = key_byte_hypothesis
            labels_key_guesses_attack_set[key_byte_hypothesis][:] = aes_intermediates(dataset.plaintext_attack,
                                                                                      dataset.ciphertext_attack,
                                                                                      key_h, self.settings["leakage_model"])

        if dataset.x_validation is not None:
            labels_key_guesses_validation_set = np.zeros((256, len(dataset.x_validation)), dtype="int64")
            for key_byte_hypothesis in range(256):
                key_h = bytearray.fromhex(self.settings["key"])
                key_h[self.settings["leakage_model"]["byte"]] = key_byte_hypothesis
                labels_key_guesses_validation_set[key_byte_hypothesis][:] = aes_intermediates(dataset.plaintext_validation,
                                                                                              dataset.ciphertext_validation,
                                                                                              key_h, self.settings["leakage_model"])
        else:
            labels_key_guesses_validation_set = None
        return labels_key_guesses_attack_set, labels_key_guesses_validation_set
