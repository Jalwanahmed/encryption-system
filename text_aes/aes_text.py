from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def derive_key(passphrase: str, salt: bytes, key_len: int = 32) -> bytes:
    return PBKDF2(passphrase, salt, dkLen=key_len, count=200_000, hmac_hash_module=SHA256)

def encrypt(plaintext: bytes, passphrase: str, key_len: int = 32) -> bytes:
    salt = get_random_bytes(16)
    key = derive_key(passphrase, salt, key_len)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return salt + cipher.nonce + tag + ciphertext

def decrypt(blob: bytes, passphrase: str, key_len: int = 32) -> bytes:
    salt, nonce, tag, ciphertext = blob[:16], blob[16:32], blob[32:48], blob[48:]
    key = derive_key(passphrase, salt, key_len)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def encrypt_file(in_path: str, out_path: str, passphrase: str, key_len: int = 32):
    with open(in_path, "rb") as f:
        data = f.read()
    with open(out_path, "wb") as f:
        f.write(encrypt(data, passphrase, key_len))

def decrypt_file(in_path: str, out_path: str, passphrase: str, key_len: int = 32):
    with open(in_path, "rb") as f:
        blob = f.read()
    with open(out_path, "wb") as f:
        f.write(decrypt(blob, passphrase, key_len))

if __name__ == "__main__":
    original = b"Hello, this is a test file for AES-GCM encryption."
    enc = encrypt(original, "my_passphrase")
    dec = decrypt(enc, "my_passphrase")
    assert dec == original, "Round-trip failed!"
    print("Text AES round-trip OK. Ciphertext length:", len(enc))