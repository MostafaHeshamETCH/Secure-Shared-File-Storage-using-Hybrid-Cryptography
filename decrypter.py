from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives.ciphers.aead import (AESCCM, AESGCM,
                                                         ChaCha20Poly1305)
from des import DesKey
import utilities


def readEncryptedKeys():
    target_file = open("raw_data/store_in_me.enc", "rb")
    encryptedKeys = b""
    for line in target_file:
        encryptedKeys = encryptedKeys + line
    target_file.close()
    return encryptedKeys


def readEncryptedText(filename):
    source_filename = 'encrypted/' + filename
    file = open(source_filename, 'rb')
    encryptedText = b""
    for line in file:
        encryptedText = encryptedText + line
    file.close()
    return encryptedText


def writePlainText(filename, plainText):
    target_filename = 'files/' + filename
    target_file = open(target_filename, 'wb')
    target_file.write(plainText)
    target_file.close()


def RCAAlgo(key):
    f = Fernet(key)
    encryptedKeys = readEncryptedKeys()
    secret_data = f.decrypt(encryptedKeys)
    return secret_data


def ChaChaAlgo(filename, key, nonce):
    aad = b"authenticated but unencrypted data"
    chacha = ChaCha20Poly1305(key)
    encryptedText = readEncryptedText(filename)
    plainText = chacha.decrypt(nonce, encryptedText, aad)
    writePlainText(filename, plainText)


def AESGCMAlgo(filename, key, nonce):
    aad = b"authenticated but unencrypted data"
    aesgcm = AESGCM(key)
    encryptedText = readEncryptedText(filename)
    plainText = aesgcm.decrypt(nonce, encryptedText, aad)
    writePlainText(filename, plainText)


def DESAlgo(filename, key):
    key0 = DesKey(key)
    raw = readEncryptedText(filename)
    plainText = key0.decrypt(raw, padding=True)
    writePlainText(filename, plainText)


def decrypter(private_key):
    utilities.empty_folder('files')
    key_1 = b""
    list_directory = utilities.list_dir('key')
    filename = './key/' + list_directory[0]
    public_key = open(filename, "rb")
    for line in public_key:
        key_1 = key_1 + line
    public_key.close()
    secret_information = RCAAlgo(key_1)
    key_list = secret_information.split(b',')
    key_2 = key_list[0]
    key_3 = key_list[1]
    key_4 = key_list[2]
    nonce12 = key_list[3]

    files = sorted(utilities.list_dir('encrypted'))
    for index in range(0, len(files)):
        if index % 3 == 0:
            AESGCMAlgo(files[index], key_3, nonce12)
        elif index % 3 == 1:
            ChaChaAlgo(files[index], key_2, nonce12)
        else:
            DESAlgo(files[index], key_4)
