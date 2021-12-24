from aisy_sca.crypto.aes.intermediates_decrypt import *
from aisy_sca.crypto.aes.intermediates_encrypt import *


def repeat_key_candidate(keys, nb_traces):
    """ repeat key if argument keys is a single key candidate (for GE and SR computations)"""
    if np.array(keys).ndim == 1:
        return np.full([nb_traces, len(keys)], keys)
    else:
        return keys


def get_round_keys(keys):
    keys = np.array(keys, dtype='uint8')
    if np.all(keys == keys[0]):
        """ If all keys are equal, then compute round keys for one key only """
        round_keys = expand_key(list(keys[0]))
        return np.full([len(keys), len(round_keys), len(round_keys[0])], round_keys)
    else:
        return [expand_key(list(key)) for key in keys]


def aes_intermediates(plaintexts, ciphertexts, keys, leakage_model):
    if "input" in leakage_model["attack_direction"]:
        if "Encryption" in leakage_model["direction"]:
            keys = repeat_key_candidate(keys, len(plaintexts))
            intermediate_values = aes_intermediates_encrypt_from_input(plaintexts, keys, leakage_model)
        else:
            keys = repeat_key_candidate(keys, len(ciphertexts))
            intermediate_values = aes_intermediates_decrypt_from_input(ciphertexts, get_round_keys(keys), leakage_model)
    else:
        if "Encryption" in leakage_model["direction"]:
            keys = repeat_key_candidate(keys, len(ciphertexts))
            intermediate_values = aes_intermediates_encrypt_from_output(ciphertexts, get_round_keys(keys), leakage_model)
        else:
            keys = repeat_key_candidate(keys, len(plaintexts))
            intermediate_values = aes_intermediates_decrypt_from_output(plaintexts, keys, leakage_model)

    if leakage_model["leakage_model"] in ["HW", "HD"]:
        return [bin(iv).count("1") for iv in intermediate_values]
    elif leakage_model["leakage_model"] == "bit":
        return [int(bin(iv >> leakage_model["bit"])[len(bin(iv >> leakage_model["bit"])) - 1]) for iv in intermediate_values]
    else:
        return intermediate_values
