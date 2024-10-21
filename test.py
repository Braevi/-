import random
from sympy import isprime, mod_inverse


# 生成一个大素数p和q
def generate_prime_number(start=100, end=200):
    while True:
        num = random.randint(start, end)
        if isprime(num):
            return num


# 生成RSA密钥对
def generate_rsa_keys():
    p = generate_prime_number()
    q = generate_prime_number()

    # 计算n和phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # 选择e（公钥指数），使得1 < e < phi(n)并且e与phi(n)互质
    e = 65537  # 常用的e值，通常选定为 65537，既是一个素数，又能确保高效性

    # 计算d（私钥指数），使得d * e ≡ 1 (mod phi(n))
    d = mod_inverse(e, phi_n)

    # 返回公钥和私钥
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


# 加密函数
def encrypt(message, public_key):
    e, n = public_key
    # 将消息转为整数并加密
    m = int.from_bytes(message.encode(), byteorder='big')
    c = pow(m, e, n)
    return c


# 解密函数
def decrypt(ciphertext, private_key):
    d, n = private_key
    # 解密得到整数
    m = pow(ciphertext, d, n)
    # 将整数转回字符串
    message = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big').decode()
    return message


# 演示RSA加密和解密
def rsa_demo():
    # 生成公钥和私钥
    public_key, private_key = generate_rsa_keys()

    print("公钥:", public_key)
    print("私钥:", private_key)

    # 输入需要加密的消息
    message = "Hello RSA!"
    print("原始消息:", message)

    # 加密
    ciphertext = encrypt(message, public_key)
    print("加密后的密文:", ciphertext)

    # 解密
    decrypted_message = decrypt(ciphertext, private_key)
    print("解密后的消息:", decrypted_message)


# 运行RSA演示
if __name__ == "__main__":
    rsa_demo()