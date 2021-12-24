class Dataset:

    def __init__(self, x_profiling, y_profiling, x_attack, y_attack, x_validation=None, y_validation=None, plaintext_profiling=None,
                 plaintext_attack=None, ciphertext_profiling=None, ciphertext_attack=None, key_profiling=None, key_attack=None,
                 plaintext_validation=None, ciphertext_validation=None, key_validation=None):
        """ set profiling, validation and attack traces"""
        self.x_profiling = x_profiling
        self.x_attack = x_attack
        self.x_validation = x_validation

        """ set profiling, validation and attack labels"""
        self.y_profiling = y_profiling
        self.y_attack = y_attack
        self.y_validation = y_validation

        """ set profiling, validation and attack plaintext"""
        self.plaintext_profiling = plaintext_profiling
        self.plaintext_attack = plaintext_attack
        self.plaintext_validation = plaintext_validation

        """ set profiling, validation and attack ciphertext"""
        self.ciphertext_profiling = ciphertext_profiling
        self.ciphertext_attack = ciphertext_attack
        self.ciphertext_validation = ciphertext_validation

        """ set profiling, validation and attack keys"""
        self.key_profiling = key_profiling
        self.key_attack = key_attack
        self.key_validation = key_validation

    def reshape_for_cnn(self):
        """ reshape traces for CNNs """
        self.x_profiling = self.x_profiling.reshape((self.x_profiling.shape[0], self.x_profiling.shape[1], 1))
        if self.x_validation is not None:
            self.x_validation = self.x_validation.reshape((self.x_validation.shape[0], self.x_validation.shape[1], 1))
        self.x_attack = self.x_attack.reshape((self.x_attack.shape[0], self.x_attack.shape[1], 1))

    def reshape_for_mlp(self):
        """ reshape traces for CNNs """
        self.x_profiling = self.x_profiling.reshape((self.x_profiling.shape[0], self.x_profiling.shape[1]))
        if self.x_validation is not None:
            self.x_validation = self.x_validation.reshape((self.x_validation.shape[0], self.x_validation.shape[1]))
        self.x_attack = self.x_attack.reshape((self.x_attack.shape[0], self.x_attack.shape[1]))
