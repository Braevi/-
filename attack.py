import itertools
import time
from SDES import SDES


def brute_force_attack(ciphertext):
    start_time = time.time()
    for i in range(1024):  # 2^10 possibilities
        key = [int(x) for x in bin(i)[2:].zfill(10)]
        sdes = SDES(key)
        decrypted = sdes.decrypt(ciphertext)
        if decrypted == [1, 0, 1, 0, 0, 1, 1, 1]:  # Example of known plaintext
            print(f"Key found: {key}")
            print(f"Time taken: {time.time() - start_time} seconds")
            return key
    print("Key not found.")