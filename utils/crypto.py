import os
from base64 import urlsafe_b64decode, urlsafe_b64encode

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv

load_dotenv()

# Carregue a chave secreta do arquivo .env
SECRET_KEY_CRIPTO = os.getenv("SECRET_KEY_CRIPTO")


def generate_fernet_key(secret_key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = urlsafe_b64encode(kdf.derive(secret_key.encode()))
    return Fernet(key)


def encrypt_number(number):
    try:
        salt = os.urandom(16)  # Gera um salt aleatório
        fernet = generate_fernet_key(SECRET_KEY_CRIPTO, salt)
        encrypted = fernet.encrypt(number.encode())
        encrypted_data = salt + encrypted
        # Codifica os dados criptografados como base64
        return urlsafe_b64encode(encrypted_data).decode()
    except Exception as e:
        print(e)
        return "Falha durante criptografia"


def decrypt_number(encrypted_number):
    try:
        if not encrypted_number:
            return ''
        # Decodifica os dados criptografados de base64
        encrypted_data = urlsafe_b64decode(encrypted_number.encode())
        salt = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        fernet = generate_fernet_key(SECRET_KEY_CRIPTO, salt)
        decrypted = fernet.decrypt(encrypted)
        return decrypted.decode()
    except Exception as e:
        print(e)
        return "Falha durante descriptografia"


if __name__ == '__main__':

    # Exemplo de uso
    number = "97788-9988"
    encrypted = encrypt_number(number)
    print(f"Nome criptografado: {encrypted}")
    decrypted = decrypt_number(encrypted)
    print(f"Nome descriptografado: {decrypted}")
