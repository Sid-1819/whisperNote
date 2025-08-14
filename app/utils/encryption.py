from cryptography.fernet import Fernet
import os

# Generate a key if not exists (for dev; in prod, set via ENV)
key_path = ".secret.key"
if os.path.exists(key_path):
    with open(key_path, "rb") as f:
        SECRET_KEY = f.read()
else:
    SECRET_KEY = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(SECRET_KEY)

fernet = Fernet(SECRET_KEY)

def encrypt_text(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            