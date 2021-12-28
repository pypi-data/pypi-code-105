import os
import logging
from halo import Halo
from waitress import serve
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def server(on_result):
    app = Flask(__name__)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    spinner = Halo(text='Waiting for browser authorization', spinner='dots')
    spinner.start()

    @app.route('/set-remote', methods=['POST'])
    def set_remote():
        public_key = get_or_create_ssh_public_key()
        spinner.stop()
        on_result(request.json['remote'])
        return jsonify({'publicKey': public_key})

    serve(app, host="0.0.0.0", port=54321)


def get_or_create_ssh_public_key():
    home = os.path.expanduser('~')
    ssh_dir = os.path.join(home, '.ssh')
    if not os.path.exists(ssh_dir):
        os.mkdir(ssh_dir)
        public_key = create_and_write_ssh_keypair()
    else:
        result = None
        find_file = False
        with open(os.path.join(home, '.ssh', 'config'), 'r') as f:
            for line in f:
                if line.startswith('gitlab.com'):
                    find_file = True
                elif find_file and line.startswith('IdentityFile ~/.ssh/'):
                    result = line.replace('IdentityFile ~/.ssh/', '')
                    break
        if result is None:
            public_key = create_and_write_ssh_keypair()
        else:
            public_key = ''
            with open(os.path.join(home, '.ssh', f'{result}.pub'), 'r') as f:
                for l in f:
                    public_key += l
                public_key = public_key.replace('\n', '')

    return public_key


def create_and_write_ssh_keypair():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    home = os.path.expanduser('~')
    ssh_dir = os.path.join(home, '.ssh')

    with open(os.path.join(ssh_dir, 'gitlab'), 'wb') as f:
        f.write(private_key)

    with open(os.path.join(ssh_dir, 'gitlab.pub'), 'wb') as f:
        f.write(public_key)

    with open(os.path.join(home, '.ssh', 'config'), 'a') as f:
        f.write(f'Host gitlab.com\n\tHostName gitlab.com\n\tIdentityFile ~/.ssh/gitlab\n')

    return public_key.decode('utf-8')
