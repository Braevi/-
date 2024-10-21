from SDES import SDES


def check_key_collision(plaintext):
    ciphertexts = {}
    for i in range(1024):
        key = [int(x) for x in bin(i)[2:].zfill(10)]
        sdes = SDES(key)
        ciphertext = sdes.encrypt(plaintext)
        cipher_tuple = tuple(ciphertext)
        if cipher_tuple in ciphertexts:
            print(f"Collision found: {ciphertexts[cipher_tuple]} and {key} produce the same ciphertext.")
        else:
            ciphertexts[cipher_tuple] = key