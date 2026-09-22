from cryptography.fernet import Fernet

def test_crypto_logic():
    key = Fernet.generate_key()
    f = Fernet(key)
    message = b"Secret message for Yocto smoke test"
    token = f.encrypt(message)
    decrypted = f.decrypt(token)
    if decrypted == message:
        print("Cryptography functional test: PASSED")
    else:
        print("Cryptography functional test: FAILED")
        exit(1)

if __name__ == "__main__":
    test_crypto_logic()