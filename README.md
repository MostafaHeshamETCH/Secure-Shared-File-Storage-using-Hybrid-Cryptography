# Secure Shared File Storage using Hybrid Cryptography

## Introduction
The purpose of this project is to build a secure file sharing platform using multiple encryption algorithms.
## Methodology
To achieve the above goal, the following methodology needs to be followed:
### File Storage:
1. Dividing the file to upload into N parts. (N depends on the file size)
2. Generate m keys randomly, where m is the number of symmetric ciphers used (at least 3 ciphers
including DES and AES, and you may choose a third one or even your own cipher)
3. Encrypting all the parts of the file using one of the selected algorithms (Algorithm is changed with
every part in round-robin fashion). And the parts are put together in a single file as ordered.
4. The keys for cryptography algorithms are then grouped in a key file and encrypted using a different algorithm and the key for this algorithm is also generated randomly and is called the file master key.
5. The data file and the key file are than uploaded to the FTP server
6. A copy of the master key is kept in a local file with the file name to be shared.
### File Retrieval:
1. A user requesting the master key must provide his public key to the owner
2. The owner then encrypts the master key of the requested file with the requesting user public key
and sends it to him
3. The user can then download the data file and the key file, decrypts the master key with his private
key and then decrypts the data file
## Tech Stack
1. [Flask](https://flask.palletsprojects.com/en/2.2.x/)
2. Pure HTML & CSS