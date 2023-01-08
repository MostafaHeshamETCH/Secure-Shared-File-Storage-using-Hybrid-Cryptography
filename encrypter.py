import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import (AESGCM, ChaCha20Poly1305)
from des import DesKey
import utilities


def readPlainText(filename) -> bytes:
    source_filename = 'files/' + filename
    file = open(source_filename, 'rb')
    raw = b""
    for line in file:
        raw = raw + line
    file.close()
    return raw


def writeEncryptedText(filename, encryptedData: bytes):
    target_filename = 'encrypted/' + filename
    target_file = open(target_filename, 'wb')
    target_file.write(encryptedData)
    target_file.close()


def writeEncryptedKeys(encryptedKeys: bytes):
    target_file = open("raw_data/store_in_me.enc", "wb")
    target_file.write(encryptedKeys)
    target_file.close()


def rsaKeyPairGeneration():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    return {"private": private_key, "public": public_key}


def RSAAlgo2(data: bytes, my_private_key, your_public_key):
    encryptedKeys = my_private_key.encrypt(data)
    encryptedKeys = your_public_key.encrypt(encryptedKeys)
    # All keys stored in store_in_me.enc encrypted with my_private_key as well as your_public_key
    writeEncryptedKeys(encryptedKeys)


def RSAAlgo(data: bytes, key: bytes):
    f = Fernet(key)
    secret_data = f.encrypt(data)
    writeEncryptedKeys(secret_data)


def DESAlgo(filename, key: bytes):
    f = DesKey(key)
    raw = readPlainText(filename)
    secret_data = f.encrypt(raw, padding=True)
    writeEncryptedText(filename, secret_data)


def ChaChaAlgo(filename, key: bytes, nonce: bytes):
    aad = b"authenticated but unencrypted data"
    cha_cha = ChaCha20Poly1305(key)

    raw = readPlainText(filename)
    encryptedData = cha_cha.encrypt(nonce, raw, aad)
    writeEncryptedText(filename, encryptedData)


def AESGCMAlgo(filename, key: bytes, nonce: bytes):
    aad = b"authenticated but unencrypted data"
    aesgcm = AESGCM(key)
    raw = readPlainText(filename)
    encryptedData = aesgcm.encrypt(nonce, raw, aad)
    writeEncryptedText(filename, encryptedData)


def encrypter(public_key):
    utilities.empty_folder('key')
    utilities.empty_folder('encrypted')
    key_1 = Fernet.generate_key()  # the downloaded public key
    key_2 = ChaCha20Poly1305.generate_key()
    key_3 = AESGCM.generate_key(bit_length=128)
    key_4 = os.urandom(8)
    files = sorted(utilities.list_dir('files'))
    nonce12 = os.urandom(12)

    keys = rsaKeyPairGeneration()
    print(keys["private"])
    print(keys["public"])

    for index in range(0, len(files)):
        if index % 3 == 0:
            AESGCMAlgo(files[index], key_3, nonce12)
        elif index % 3 == 1:
            ChaChaAlgo(files[index], key_2, nonce12)  # ChaCha Encryption Algorithm
        else:
            DESAlgo(files[index], key_4)

    secret_information = key_2 + b"," + key_3 + b"," + key_4 + b"," + nonce12

    # Encrypting all the keys with algo1 using key_1
    RSAAlgo(secret_information, key_1)
    public_key = open("./key/secret_upload_key.pem", "wb")
    public_key.write(key_1)  # key_1 stored in Main_Key.pem
    public_key.close()
    utilities.empty_folder('files')
