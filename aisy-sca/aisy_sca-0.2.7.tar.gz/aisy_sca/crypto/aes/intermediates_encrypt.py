from aisy_sca.crypto.aes.aes128 import *


def aes_intermediates_encrypt_from_input(plaintexts, keys, leakage_model):
    if leakage_model["leakage_model"] in ["HD", "HD_ID", "HD_bit"]:
        return get_hd_intermediates_encrypt_input(plaintexts, keys, leakage_model)
    elif leakage_model["leakage_model"] in ["HW", "ID", "bit"]:
        return get_hw_id_intermediates_encrypt_input(plaintexts, keys, leakage_model)
    else:
        print("Leakage model not supported!")
        return None


def aes_intermediates_encrypt_from_output(ciphertexts, keys, leakage_model):
    if leakage_model["leakage_model"] in ["HD", "HD_ID", "HD_bit"]:
        return get_hd_intermediates_encrypt_output(ciphertexts, keys, leakage_model)
    elif leakage_model["leakage_model"] in ["HW", "ID", "bit"]:
        return get_hw_id_intermediates_encrypt_output(ciphertexts, keys, leakage_model)
    else:
        print("Leakage model not supported!")
        return None


def get_sbox_in_xor_sbox_out_encrypt_input(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    state1 = [int(p) ^ int(k) for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]
    state2 = s_box[state1]
    return [int(s1) ^ int(s2) for s1, s2 in zip(np.asarray(state1[:]), np.asarray(state2[:]))]


def get_sbox_in_xor_mixcolumns_out_encrypt_input(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state1 = []
    state2 = []
    for plaintext, key in zip(plaintexts, keys):
        state = add_round_key(plaintext, key)
        state1.append(state)
        state = sub_bytes(state)
        state = shift_rows(state)
        state2.append(mix_columns(state))
    return [int(inv_shift_rows(s1)[leakage_model["byte"]]) ^ int(s2[leakage_model["byte"]]) for s1, s2 in
            zip(np.asarray(state1[:]), np.asarray(state2[:]))]


def get_addroundkey_out_encrypt_input(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [int(p) ^ int(k) for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_sbox_out_encrypt_input(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [s_box[int(p) ^ int(k)] for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_shiftrows_out_encrypt_input(leakage_model, plaintexts, keys):
    plaintext = [row[inv_shift_row_mask[leakage_model["byte"]]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [s_box[int(p) ^ int(k)] for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_mixcolumns_out_encrypt_input(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state_mc = []
    for plaintext, key in zip(plaintexts, keys):
        state = add_round_key(plaintext, key)
        state = sub_bytes(state)
        state = shift_rows(state)
        state_mc.append(mix_columns(state))
    return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_mc]


def get_addroundkey_out_encrypt_input_round_2(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state_add_round_key = []
    for plaintext, key in zip(plaintexts, keys):
        round_keys = expand_key(key.copy())
        state = add_round_key(plaintext, key)
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state_add_round_key.append(add_round_key(state, round_keys[1]))  # todo: compute the constant value for rk1
    return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_add_round_key]


def get_sbox_out_encrypt_input_round_2(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state_sbox = []
    for plaintext, key in zip(plaintexts, keys):
        round_keys = expand_key(key.copy())
        state = add_round_key(plaintext, round_keys[0])
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[1])  # todo: compute the constant value for rk1
        state_sbox.append(sub_bytes(state))
    return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_sbox]


def get_hd_intermediates_encrypt_input(plaintexts, keys, leakage_model):
    """
            There is support for the following leakage models:
            - HD(SboxIn XOR SboxOut) or SboxIn XOR SboxOut
            - HD(SboxIn XOR MixColumnsOut) or SboxIn XOR MixColumnsOut
            """
    if leakage_model["target_state_first"] == "AddRoundKey" and leakage_model["target_state_second"] == "Sbox" and leakage_model[
        "round_first"] == 1:
        return get_sbox_in_xor_sbox_out_encrypt_input(leakage_model, plaintexts, keys)
    elif leakage_model["target_state_first"] == "AddRoundKey" and leakage_model["target_state_second"] == "MixColumns" and \
            leakage_model["round_first"] == 1:
        return get_sbox_in_xor_mixcolumns_out_encrypt_input(leakage_model, plaintexts, keys)
    else:
        print("Leakage model not supported!")
        return None


def get_hw_id_intermediates_encrypt_input(plaintexts, keys, leakage_model):
    if leakage_model["round"] == 1:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_out_encrypt_input(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "Sbox":
            return get_sbox_out_encrypt_input(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "ShiftRows":
            return get_shiftrows_out_encrypt_input(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "MixColumns":
            return get_mixcolumns_out_encrypt_input(leakage_model, plaintexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    elif leakage_model["round"] == 2:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_out_encrypt_input_round_2(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "Sbox":
            return get_sbox_out_encrypt_input_round_2(leakage_model, plaintexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None


def get_sbox_in_xor_output_encrypt_output(leakage_model, ciphertexts, keys):
    state1 = [row[shift_row_mask[leakage_model["byte"]]] for row in ciphertexts]
    ciphertext = [row[leakage_model["byte"]] for row in ciphertexts]
    key = [row[10][leakage_model["byte"]] for row in keys]
    return [inv_s_box[int(c1) ^ int(k)] ^ int(c2) for c1, c2, k in zip(np.asarray(ciphertext[:]), np.asarray(state1[:]),
                                                                       np.asarray(key[:]))]


def get_sbox_in_xor_sbox_out_encrypt_output(leakage_model, ciphertexts, keys):
    ciphertext = [row[shift_row_mask[leakage_model["byte"]]] for row in ciphertexts]
    key = [row[10][leakage_model["byte"]] for row in keys]
    state1 = [int(c) ^ int(k) for c, k in zip(np.asarray(ciphertext[:]), np.asarray(key[:]))]
    state2 = inv_s_box[state1]
    return [int(s1) ^ int(s2) for s1, s2 in zip(np.asarray(state1[:]), np.asarray(state2[:]))]


def get_addroundkey_in_encrypt_output(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_add_round_key = []
    for ciphertext, key in zip(ciphertexts, keys):
        state_add_round_key.append(add_round_key(ciphertext, key[10]))
    return [int(s[leakage_model["byte"]]) for s in state_add_round_key]


def get_shiftrows_in_encrypt_output(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_shiftrows = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state_shiftrows.append(inv_shift_rows(state))
    return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_shiftrows]


def get_sbox_in_in_encrypt_output(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_sbox = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state = inv_shift_rows(state)
        state_sbox.append(inv_sub_bytes(state))
    return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_sbox]


def get_addroundkey_in_encrypt_output_round_9(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_add_round_key = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state_add_round_key.append(add_round_key(state, key[9]))  # todo: compute the constant value for rk1
    return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_add_round_key]


def get_mixcolumns_in_encrypt_output_round_9(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(ciphertexts, dtype=np.uint8)
    state_mc = []
    for ciphertext, key in zip(plaintexts, keys):
        state = add_round_key(ciphertext, key[10])
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key[9])  # todo: compute the constant value for rk1
        state_mc.append(inv_mix_columns(state))
    return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_mc]


def get_hd_intermediates_encrypt_output(ciphertexts, keys, leakage_model):
    """
        There is support for the following leakage models:
        - HD(SboxIn XOR Ciphertext) or SboxIn XOR Ciphertext
        - HD(SboxIn XOR SboxOut) or SboxIn XOR SboxOut
    """
    if leakage_model["round_first"] == 10:
        if leakage_model["target_state_first"] == "Output" and leakage_model["target_state_second"] == "Sbox":
            return get_sbox_in_xor_output_encrypt_output(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state_first"] == "AddRoundKey" and leakage_model["target_state_second"] == "Sbox":
            return get_sbox_in_xor_sbox_out_encrypt_output(leakage_model, ciphertexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None


def get_hw_id_intermediates_encrypt_output(ciphertexts, keys, leakage_model):
    if leakage_model["round"] == 10:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_in_encrypt_output(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "InvShiftRows":
            return get_shiftrows_in_encrypt_output(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "InvSbox":
            return get_sbox_in_in_encrypt_output(leakage_model, ciphertexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    elif leakage_model["round"] == 9:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_in_encrypt_output_round_9(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "invMixColumns":
            return get_mixcolumns_in_encrypt_output_round_9(leakage_model, ciphertexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None
