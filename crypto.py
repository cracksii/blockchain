from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature
import codecs
import os
from config import PASSWORD_SIZE, KEY_SIZE


def generate_password():
    return codecs.encode(os.urandom(PASSWORD_SIZE), "base64").decode()


def generate_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
        backend=default_backend()
    )


def generate_private_pem(private_key, password):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password=password
        )
    )


def generate_public_key(private_key):
    return private_key.public_key()


def generate_public_pem(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def generate_private_pem_string(password_string):
    private_key = generate_private_key()
    pem = generate_private_pem(private_key, password_string.encode("utf-8"))
    return pem.decode()


def generate_public_pem_string(private_pem_string, password_string):
    private_key = load_private_key(
        private_pem=private_pem_string.encode("utf-8"),
        password=password_string.encode("utf-8")
    )
    public_key = generate_public_key(private_key)
    return generate_public_pem(public_key).decode()


def load_private_key(private_pem, password):
    return serialization.load_pem_private_key(
        data=private_pem,
        password=password,
        backend=default_backend()
    )


def load_public_key(public_pem):
    return serialization.load_pem_public_key(
        data=public_pem,
        backend=default_backend()
    )


def verify(public_pem_string, signature_string, data_string):
    public_key = load_public_key(public_pem_string.encode("utf-8"))
    signature_binary = codecs.decode(signature_string.encode("utf-8"), "base64")
    return verify_binary(public_key, signature_binary, data_string.encode("utf-8"))


def verify_binary(public_key, signature, data):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA3_256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA3_256()
        )
    except InvalidSignature:
        return False
    return True


def sign(private_pem_string, password_string, data_string):
    private_key = load_private_key(private_pem_string.encode("utf-8"), password_string.encode("utf-8"))
    signature = sign_binary(private_key, data_string.encode("utf-8"))
    return codecs.encode(signature, "base64").decode()


def sign_binary(private_key, data):
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA3_256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA3_256()
    )
