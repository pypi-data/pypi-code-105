from aisy_sca.crypto.aes.aes128 import *


def aes_intermediates_decrypt_from_input(ciphertexts, keys, leakage_model):
    if leakage_model["leakage_model"] in ["HD", "HD_ID", "HD_bit"]:
        return get_hd_intermediates_decrypt_input(ciphertexts, keys, leakage_model)
    elif leakage_model["leakage_model"] in ["HW", "ID", "bit"]:
        return get_hw_id_intermediates_decrypt_input(ciphertexts, keys, leakage_model)
    else:
        print("Leakage model not supported!")
        return None


def aes_intermediates_decrypt_from_output(plaintexts, keys, leakage_model):
    if leakage_model["leakage_model"] in ["HD", "HD_ID", "HD_bit"]:
        return get_hd_intermediates_decrypt_output(plaintexts, keys, leakage_model)
    elif leakage_model["leakage_model"] in ["HW", "ID", "bit"]:
        return get_hw_id_intermediates_decrypt_output(plaintexts, keys, leakage_model)
    else:
        print("Leakage model not supported!")
        return None


def get_input_xor_sbox_out_decrypt_input(leakage_model, ciphertexts, keys):
    state1 = [row[inv_shift_row_mask[leakage_model["byte"]]] for row in ciphertexts]
    ciphertext = [row[leakage_model["byte"]] for row in ciphertexts]
    key = [row[10][leakage_model["byte"]] for row in keys]
    return [inv_s_box[int(c1) ^ int(k)] ^ int(c2) for c1, c2, k in zip(np.asarray(state1[:]), np.asarray(ciphertext[:]),
                                                                       np.asarray(key[:]))]


def get_sbox_in_xor_sbox_out_decrypt_input(leakage_model, ciphertexts, keys):
    ciphertext = [row[inv_shift_row_mask[leakage_model["byte"]]] for row in ciphertexts]
    key = [row[10][leakage_model["byte"]] for row in keys]
    state1 = [int(c) ^ int(k) for c, k in zip(np.asarray(ciphertext[:]), np.asarray(key[:]))]
    state2 = inv_s_box[state1]
    return [int(s1) ^ int(s2) for s1, s2 in zip(np.asarray(state1[:]), np.asarray(state2[:]))]


def get_addroundkey_out_decrypt_input(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_add_round_key = []
    for ciphertext, key in zip(ciphertexts, keys):
        state_add_round_key.append(add_round_key(ciphertext, key[10]))
    return [int(s[leakage_model["byte"]]) for s in state_add_round_key]


def get_inv_shiftrows_out_decrypt_input(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_add_round_key = []
    for ciphertext, key in zip(ciphertexts, keys):
        state_add_round_key.append(add_round_key(ciphertext, key[10]))
    return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_add_round_key]


def get_inv_sbox_out_decrypt_input(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_inv_sbox = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state_inv_sbox.append(inv_sub_bytes(state))
    return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_inv_sbox]


def get_addroundkey_out_decrypt_input_round_2(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_add_round_key = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state_add_round_key.append(add_round_key(state, key[9]))  # todo: compute the constant value for rk9
        return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_add_round_key]


def get_inv_mixcolumns_out_decrypt_input_round_2(leakage_model, ciphertexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    ciphertexts = np.array(ciphertexts, dtype=np.uint8)
    state_mc = []
    for ciphertext, key in zip(ciphertexts, keys):
        state = add_round_key(ciphertext, key[10])
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key[9])  # todo: compute the constant value for rk9
        state_mc.append(inv_mix_columns(state))
    return [int(s[shift_row_mask[leakage_model["byte"]]]) for s in state_mc]


def get_hd_intermediates_decrypt_input(ciphertexts, keys, leakage_model):
    """
    There is support for the following leakage models:
    - HD(SboxIn XOR Ciphertext) or SboxIn XOR Ciphertext
    - HD(SboxIn XOR SboxOut) or SboxIn XOR SboxOut
    """
    if leakage_model["round_first"] == 1:
        if leakage_model["target_state_first"] == "Input" and leakage_model["target_state_second"] == "InvSbox":
            return get_input_xor_sbox_out_decrypt_input(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state_first"] == "AddRoundKey" and leakage_model["target_state_second"] == "InvSbox":
            return get_sbox_in_xor_sbox_out_decrypt_input(leakage_model, ciphertexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None


def get_hw_id_intermediates_decrypt_input(ciphertexts, keys, leakage_model):
    if leakage_model["round"] == 1:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_out_decrypt_input(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "InvShiftRows":
            return get_inv_shiftrows_out_decrypt_input(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "InvSbox":
            return get_inv_sbox_out_decrypt_input(leakage_model, ciphertexts, keys)
    elif leakage_model["round"] == 2:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_out_decrypt_input_round_2(leakage_model, ciphertexts, keys)
        elif leakage_model["target_state"] is "InvMixColumns":
            return get_inv_mixcolumns_out_decrypt_input_round_2(leakage_model, ciphertexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None


def get_output_xor_sbox_in_decrypt_output(leakage_model, plaintexts, keys):
    state1 = [row[leakage_model["byte"]] for row in plaintexts]
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [s_box[int(p1) ^ int(k)] ^ int(p2) for p1, p2, k in zip(np.asarray(state1[:]), np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_sbox_in_xor_sbox_out_decrypt_output(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    state1 = [int(p) ^ int(k) for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]
    state2 = s_box[state1]
    return [int(s1) ^ int(s2) for s1, s2 in zip(np.asarray(state1[:]), np.asarray(state2[:]))]


def get_addroundkey_in_decrypt_output(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [int(p) ^ int(k) for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_inv_sbox_in_decrypt_output(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [s_box[int(p) ^ int(k)] for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_inv_shiftrows_in_decrypt_output(leakage_model, plaintexts, keys):
    plaintext = [row[leakage_model["byte"]] for row in plaintexts]
    key = [row[leakage_model["byte"]] for row in keys]
    return [inv_s_box[int(p) ^ int(k)] for p, k in zip(np.asarray(plaintext[:]), np.asarray(key[:]))]


def get_inv_mixcolumns_in_decrypt_output_round_9(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state_mc = []
    for plaintext, key in zip(plaintexts, keys):
        round_keys = expand_key(key.copy())
        state = add_round_key(plaintext, round_keys[0])
        state = sub_bytes(state)
        state = shift_rows(state)
        state_mc.append(mix_columns(state))
        return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_mc]


def get_addroundkey_in_decrypt_output_round_9(leakage_model, plaintexts, keys):
    keys = np.array(keys, dtype=np.uint8)
    plaintexts = np.array(plaintexts, dtype=np.uint8)
    state_add_round_key = []
    for plaintext, key in zip(plaintexts, keys):
        round_keys = expand_key(key.copy())
        state = add_round_key(plaintext, round_keys[0])
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state_add_round_key.append(add_round_key(state, round_keys[1]))  # todo: compute the constant value for rk1
        return [int(s[inv_shift_row_mask[leakage_model["byte"]]]) for s in state_add_round_key]


def get_inv_sbox_in_decrypt_output_round_9(leakage_model, plaintexts, keys):
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


def get_inv_shiftrows_in_decrypt_output_round_9(leakage_model, plaintexts, keys):
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


def get_hd_intermediates_decrypt_output(plaintexts, keys, leakage_model):
    """
    There is support for the following leakage models:
    - HD(SboxIn XOR Ciphertext) or SboxIn XOR Ciphertext
    - HD(SboxIn XOR SboxOut) or SboxIn XOR SboxOut
    """
    if leakage_model["round_first"] == 1:
        if leakage_model["target_state_first"] == "Output" and leakage_model["target_state_second"] == "InvSbox":
            return get_output_xor_sbox_in_decrypt_output(leakage_model, plaintexts, keys)
        elif leakage_model["target_state_first"] == "AddRoundKey" and leakage_model["target_state_second"] == "InvSbox":
            return get_sbox_in_xor_sbox_out_decrypt_output(leakage_model, plaintexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None


def get_hw_id_intermediates_decrypt_output(plaintexts, keys, leakage_model):
    if leakage_model["round"] == 10:
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_in_decrypt_output(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "InvSbox":
            return get_inv_sbox_in_decrypt_output(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "InvShiftRows":
            return get_inv_shiftrows_in_decrypt_output(leakage_model, plaintexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    elif leakage_model["round"] == 9:
        if leakage_model["target_state"] is "InvMixColumns":
            return get_inv_mixcolumns_in_decrypt_output_round_9(leakage_model, plaintexts, keys)
        if leakage_model["target_state"] is "AddRoundKey":
            return get_addroundkey_in_decrypt_output_round_9(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "InvSbox":
            return get_inv_sbox_in_decrypt_output_round_9(leakage_model, plaintexts, keys)
        elif leakage_model["target_state"] is "InvShiftRows":
            return get_inv_shiftrows_in_decrypt_output_round_9(leakage_model, plaintexts, keys)
        else:
            print("Leakage model not supported!")
            return None
    else:
        print("Leakage model not supported!")
        return None
