import json
import cryptography.fernet
from cryptography.fernet import Fernet
from getpass import getpass
import os
from pathlib import Path
import base64
from hashlib import md5
from typing import List
from config import PRIVATE_KEYS_PATH, WALLETS_PATH, ENCRYPTED_DATA_PATH


def generate_key_from_password(password: str) -> bytes:
    md5_password = md5(password.encode()).hexdigest()
    return base64.urlsafe_b64encode(md5_password.encode())


def get_user_password(is_keys_encrypted: bool) -> bytes:
    """
    Simple interface for getting password from user input
    :param is_keys_encrypted: True if keys are encrypted
    :return: key
    """
    if is_keys_encrypted:
        password = getpass('Enter the password: ')
    else:
        while True:
            password = getpass('Create password: ')
            password_verif = getpass('Verify password: ')
            if password != password_verif:
                print('Verification failed')
                continue
            break
    return generate_key_from_password(password)


def get_private_keys_from_wallets(password) -> List[str]:

    # read wallet data
    encrypted_data_path = Path(ENCRYPTED_DATA_PATH)
    wallets_path = Path(WALLETS_PATH)

    if not encrypted_data_path.exists():
        raise ValueError(f'File does not exist {encrypted_data_path}')
    if not wallets_path.exists():
        raise ValueError(f'File does not exist {encrypted_data_path}')

    with open(encrypted_data_path, 'rb') as f:
        encoded_keys = f.read()
    with open(wallets_path, 'r') as f:
        wallets = [wallet.lower() for wallet in f.read().split()]

    fernet = Fernet(password)
    wallet_data = json.loads(fernet.decrypt(encoded_keys).decode())

    # check encrypted data
    private_keys = []
    missed_wallets = []
    for wallet in wallets:
        if wallet in wallet_data:
            private_keys.append(wallet_data[wallet])
        else:
            missed_wallets.append(wallet)
    if missed_wallets:
        print(f'This wallets are not encrypted. Please, use encrypt module')
        print('\n'.join(missed_wallets))

    return private_keys


def encrypt_private_keys(password: bytes):
    wallets_path = Path(WALLETS_PATH)
    private_path = Path(PRIVATE_KEYS_PATH)

    if not private_path.exists():
        raise ValueError(f"File does not exist {private_path}")
    if not wallets_path.exists():
        raise ValueError(f"File does not exist {private_path}")

    with open(private_path, 'r') as f:
        private_keys = f.read().split()
    with open(wallets_path, 'r') as f:
        wallets = [wallet.lower() for wallet in f.read().split()]

    if len(private_keys) != len(wallets):
        raise ValueError(f'Length of wallets != length of private keys')

    wallet_data = dict(zip(wallets, private_keys))
    fernet = Fernet(password)
    encrypted_data = fernet.encrypt(json.dumps(wallet_data).encode())
    with open(ENCRYPTED_DATA_PATH, 'wb') as f:
        f.write(encrypted_data)

    # clear private keys
    with open(private_path, 'w'):
        pass


def get_private_keys() -> List:
    n_attempts = 3
    is_keys_encrypted = os.path.exists(ENCRYPTED_DATA_PATH)

    for _ in range(n_attempts):
        try:
            password = get_user_password(is_keys_encrypted)
            if not is_keys_encrypted:
                encrypt_private_keys(password)
            privates = get_private_keys_from_wallets(password)
            break
        except cryptography.fernet.InvalidToken:
            print('Wrong Password')
    else:
        raise ValueError('Wrong password')
    return privates


if __name__ == '__main__':
    get_private_keys()
