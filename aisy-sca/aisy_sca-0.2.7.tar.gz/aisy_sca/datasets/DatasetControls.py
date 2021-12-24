from aisy_sca.datasets import Dataset
from tensorflow.keras.utils import to_categorical
from aisy_sca.crypto.sca_aes_create_intermediates import *
import h5py


class DatasetControls:

    def __init__(self, settings, split_training_set_ratio=0.9, apply_znorm=True):
        self.x_profiling = None
        self.x_validation = None
        self.x_attack = None
        self.y_profiling = None
        self.y_validation = None
        self.y_attack = None
        self.plaintext_profiling = None
        self.plaintext_validation = None
        self.plaintext_attack = None
        self.ciphertext_profiling = None
        self.ciphertext_validation = None
        self.ciphertext_attack = None
        self.key_profiling = None
        self.key_validation = None
        self.key_attack = None
        self.settings = settings
        self.split_training_set_ratio = split_training_set_ratio
        self.apply_znorm = apply_znorm

    def read(self):

        if ".h5" not in self.settings["filename"]:
            print("ERROR 10: Dataset format not supported.")
            return

        """
        Read h5 dataset with the following structure and metadata:
        [Profiling_traces/traces]
        [Profiling_traces/metadata][plaintext]
        [Profiling_traces/metadata][key]
        [Profiling_traces/metadata][ciphertext] (if exists)
        [Attack_traces/traces]
        [Attack_traces/metadata][plaintext]
        [Attack_traces/metadata][key]
        [Attack_traces/metadata][ciphertext] (if exists)
        """

        """ Define main settings"""

        nt = self.settings["number_of_profiling_traces"]
        na = self.settings["number_of_attack_traces"]
        fs = self.settings['first_sample']
        ns = self.settings['number_of_samples']

        """ Read file and get traces and metadata """

        in_file = h5py.File(f"{self.settings['datasets_root_folder']}{self.settings['filename']}", "r")
        self.x_profiling = np.array(in_file['Profiling_traces/traces'], dtype=np.float64)[:nt, fs:fs + ns]
        self.x_attack = np.array(in_file['Attack_traces/traces'], dtype=np.float64)[:na, fs:fs + ns]
        self.plaintext_profiling = in_file['Profiling_traces/metadata']['plaintext'][:nt]
        self.plaintext_attack = in_file['Attack_traces/metadata']['plaintext'][:na]
        self.key_profiling = in_file['Profiling_traces/metadata']['key'][:nt]
        self.key_attack = in_file['Attack_traces/metadata']['key'][:na]

        """ if ciphertext is in metadata """
        if "ciphertext" in in_file['Profiling_traces/metadata'].dtype.fields:
            self.ciphertext_profiling = in_file['Profiling_traces/metadata']['ciphertext'][:nt]
            self.ciphertext_attack = in_file['Attack_traces/metadata']['ciphertext'][:na]

        self.create_labels(self.settings)

        """ Split datasets if required """
        if self.settings["split_test_set"]:
            self.split_test_data(na)
        elif self.settings["split_training_set"]:
            self.split_training_data(nt, self.split_training_set_ratio)

        """ Convert to categorical labels """
        self.y_profiling = to_categorical(self.y_profiling, num_classes=self.settings["classes"])
        if self.y_validation is not None:
            self.y_validation = to_categorical(self.y_validation, num_classes=self.settings["classes"])
        self.y_attack = to_categorical(self.y_attack, num_classes=self.settings["classes"])

        if self.apply_znorm:
            self.apply_znorm_dataset()

    def create_labels(self, settings):

        if settings["leakage_model"]["cipher"] == "AES128":
            self.y_profiling = aes_intermediates(self.plaintext_profiling, self.ciphertext_profiling, self.key_profiling,
                                                 settings["leakage_model"])
            self.y_attack = aes_intermediates(self.plaintext_attack, self.ciphertext_attack, self.key_attack,
                                              settings["leakage_model"])
        else:
            print("ERROR: cipher not supported.")
            return

    def split_test_data(self, na):

        self.x_validation = self.x_attack[0: int(na / 2)]
        self.y_validation = self.y_attack[0: int(na / 2)]
        self.x_attack = self.x_attack[int(na / 2): na]
        self.y_attack = self.y_attack[int(na / 2): na]

        self.plaintext_validation = self.plaintext_attack[0: int(na / 2)]
        self.plaintext_attack = self.plaintext_attack[int(na / 2): na]

        if self.ciphertext_attack is not None:
            self.ciphertext_validation = self.ciphertext_attack[0: int(na / 2)]
            self.ciphertext_attack = self.ciphertext_attack[int(na / 2): na]

        self.key_validation = self.key_attack[0: int(na / 2)]
        self.key_attack = self.key_attack[int(na / 2): na]

    def split_training_data(self, nt, ratio):

        nt = int(nt * ratio)

        self.x_validation = self.x_profiling[nt:]
        self.y_validation = self.y_profiling[nt:]
        self.x_profiling = self.x_profiling[:nt]
        self.y_profiling = self.y_profiling[:nt]

        self.plaintext_validation = self.plaintext_profiling[nt:]
        self.plaintext_profiling = self.plaintext_profiling[:nt]

        if self.ciphertext_attack is not None:
            self.ciphertext_validation = self.ciphertext_profiling[nt:]
            self.ciphertext_profiling = self.ciphertext_profiling[:nt]

        self.key_validation = self.key_profiling[nt:]
        self.key_profiling = self.key_profiling[:nt]

    def create_z_score_norm(self, dataset):
        return np.mean(dataset, axis=0), np.std(dataset, axis=0)

    def apply_z_score_norm(self, dataset, mean, std):
        for index in range(len(dataset)):
            dataset[index] = (dataset[index] - mean) / std

    def apply_znorm_dataset(self):

        mean, std = self.create_z_score_norm(self.x_profiling)
        self.apply_z_score_norm(self.x_profiling, mean, std)
        if self.x_validation is not None:
            self.apply_z_score_norm(self.x_validation, mean, std)
        self.apply_z_score_norm(self.x_attack, mean, std)

        self.x_profiling = self.x_profiling.astype('float32')
        if self.x_validation is not None:
            self.x_validation = self.x_validation.astype('float32')
        self.x_attack = self.x_attack.astype('float32')

    def get_traces(self):
        return self.x_profiling, self.x_validation, self.x_attack

    def get_labels(self):
        return self.y_profiling, self.y_validation, self.y_attack

    def get_plaintexts(self):
        return self.plaintext_profiling, self.plaintext_validation, self.plaintext_attack

    def get_ciphertexts(self):
        return self.ciphertext_profiling, self.ciphertext_validation, self.ciphertext_attack

    def get_keys(self):
        return self.key_profiling, self.key_validation, self.key_attack

    def get_dataset(self):
        return Dataset(self.x_profiling, self.y_profiling, self.x_attack, self.y_attack, self.x_validation, self.y_validation,
                       self.plaintext_profiling, self.plaintext_attack, self.ciphertext_profiling, self.ciphertext_attack,
                       self.key_profiling, self.key_attack, self.plaintext_validation, self.ciphertext_validation, self.key_validation)
