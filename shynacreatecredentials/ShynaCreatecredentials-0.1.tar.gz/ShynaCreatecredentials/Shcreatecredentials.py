import os
import sys
from cryptography.fernet import Fernet


class CreateCredentials:
    return_status = ''
    cred_filename = ""
    key_file = ""

    def create_credential(self, password_d):
        key = Fernet.generate_key()
        f = Fernet(key)
        # key_file = "key_bot.key"
        password = f.encrypt(password_d.encode()).decode()
        with open(self.cred_filename, 'w') as file_in:
            file_in.write("{}".format(password))
        if os.path.exists(self.key_file):
            os.remove(self.key_file)
        try:
            with open(self.key_file, 'w') as key_in:
                key_in.write(key.decode())
        except PermissionError:
            os.remove(self.key_file)
            sys.exit()

    def read_credentials(self):
        with open(self.key_file, 'r') as key_in:
            key = key_in.read().encode()

        f = Fernet(key)
        with open(self.cred_filename, 'r') as cred_in:
            lines = cred_in.readline()
            self.return_status = f.decrypt(lines.encode()).decode()
        return self.return_status
