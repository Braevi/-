import itertools
import time
from SDES import SDES  # 引入SDES类


def sdes_encrypt(key, plaintext):
    """使用给定的密钥加密明文并返回密文"""
    sdes = SDES(key)
    return sdes.encrypt(plaintext)


def brute_force_attack(plaintext, ciphertext):
    """暴力破解函数，返回找到的密钥和所用时间"""
    start_time = time.time()
    keys_found = []
    key_length = 10

    # 生成所有可能的10位密钥
    for key_tuple in itertools.product([0, 1], repeat=key_length):
        key = list(key_tuple)
        # 加密明文以获得密文
        encrypted = sdes_encrypt(key, plaintext)

        if encrypted == ciphertext:
            keys_found.append(key)

    end_time = time.time()
    duration = end_time - start_time
    return keys_found, duration