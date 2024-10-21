import tkinter as tk
from tkinter import messagebox
from SDES import SDES  # 确保 SDES 类在 sdes.py 中实现
from attack import brute_force_attack  # 确保暴力破解在 attack.py 中实现
from collision import check_key_collision  # 确保冲突检测在 collision.py 中实现


def string_to_bit_array(s):
    """将字符串转换为二进制位数组"""
    return [int(bit) for char in s for bit in format(ord(char), '08b')]


def bit_array_to_string(bits):
    """将二进制位数组转换为字符串"""
    chars = [chr(int(''.join(map(str, bits[i:i + 8])), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)


def encrypt_data_normal():
    try:
        plaintext = entry_plaintext_normal.get().strip()
        key = list(map(int, entry_key_normal.get().strip()))

        if len(key) != 10:
            raise ValueError("密钥必须是10位。")

        if len(plaintext) != 8:
            raise ValueError("明文必须是8位。")

        plaintext_bits = list(map(int, plaintext))

        sdes = SDES(key)
        ciphertext = sdes.encrypt(plaintext_bits)

        ciphertext_str = ''.join(map(str, ciphertext))
        print(f"加密明文: {plaintext} -> 密文: {ciphertext_str}")  # 输出到终端
        messagebox.showinfo("密文", "密文: " + ciphertext_str)
    except Exception as e:
        messagebox.showerror("错误", str(e))


def decrypt_data_normal():
    try:
        ciphertext = entry_decrypt_ciphertext_normal.get().strip()
        key = list(map(int, entry_key_decrypt_normal.get().strip()))

        if len(key) != 10:
            raise ValueError("密钥必须是10位。")

        if len(ciphertext) != 8:
            raise ValueError("密文必须是8位。")

        ciphertext_bits = list(map(int, ciphertext))

        sdes = SDES(key)
        decrypted_bits = sdes.decrypt(ciphertext_bits)

        decrypted_str = ''.join(map(str, decrypted_bits))
        print(f"解密密文: {ciphertext} -> 明文: {decrypted_str}")  # 输出到终端
        messagebox.showinfo("解密明文", "解密明文: " + decrypted_str)
    except Exception as e:
        messagebox.showerror("错误", str(e))


def encrypt_data_ascii():
    try:
        plaintext = entry_plaintext_ascii.get().strip()
        key = list(map(int, entry_key_ascii.get().strip()))

        if len(key) != 10:
            raise ValueError("密钥必须是10位。")

        # Convert each character to 8-bit binary and encrypt
        plaintext_bits = string_to_bit_array(plaintext)
        ciphertext_bits = []

        sdes = SDES(key)

        for i in range(0, len(plaintext_bits), 8):
            block = plaintext_bits[i:i + 8]
            if len(block) < 8:
                # 如果最后一组不满8位，可以选择填充或直接跳过
                continue
            encrypted_block = sdes.encrypt(block)
            ciphertext_bits.extend(encrypted_block)

        # Convert ciphertext bits back to an ASCII string
        ciphertext_str = bit_array_to_string(ciphertext_bits)
        print(f"加密明文: {plaintext} -> 密文（ASCII）: {ciphertext_str}")  # 输出到终端
        messagebox.showinfo("密文（ASCII）", "密文（ASCII）: " + ciphertext_str)
    except Exception as e:
        messagebox.showerror("错误", str(e))


def decrypt_data_ascii():
    try:
        ciphertext = entry_decrypt_ciphertext_ascii.get().strip()
        key = list(map(int, entry_key_decrypt_ascii.get().strip()))

        if len(key) != 10:
            raise ValueError("密钥必须是10位。")

        # Convert ASCII string to binary array
        ciphertext_bits = string_to_bit_array(ciphertext)
        decrypted_bits = []

        sdes = SDES(key)

        for i in range(0, len(ciphertext_bits), 8):
            block = ciphertext_bits[i:i + 8]
            if len(block) < 8:
                continue
            decrypted_block = sdes.decrypt(block)
            decrypted_bits.extend(decrypted_block)

        # Convert decrypted bits back to an ASCII string
        decrypted_str = bit_array_to_string(decrypted_bits)
        print(f"解密密文（ASCII）: {ciphertext} -> 明文: {decrypted_str}")  # 输出到终端
        messagebox.showinfo("解密明文（ASCII）", "解密明文（ASCII）: " + decrypted_str)
    except Exception as e:
        messagebox.showerror("错误", str(e))


def perform_brute_force_attack():
    try:
        ciphertext = entry_attack_ciphertext.get().strip()
        key_length = 10  # S-DES key length
        keys = brute_force_attack(ciphertext, key_length)
        result = '\n'.join(keys)
        print(f"暴力破解结果: {result}")  # 输出到终端
        messagebox.showinfo("暴力破解结果", f"找到的密钥:\n{result}")
    except Exception as e:
        messagebox.showerror("错误", str(e))


def find_collision_data():
    try:
        input_data = entry_collision_input.get().strip()
        collisions = check_key_collision(input_data)
        result = '\n'.join(collisions)
        print(f"冲突结果: {result}")  # 输出到终端
        messagebox.showinfo("冲突结果", f"找到的冲突:\n{result}")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# GUI Setup
root = tk.Tk()
root.title("S-DES 和 ASCII 转换器")

# Normal Encrypt Section
tk.Label(root, text="输入要加密的8位明文:").pack()
entry_plaintext_normal = tk.Entry(root)
entry_plaintext_normal.pack()

tk.Label(root, text="密钥（10位）:").pack()
entry_key_normal = tk.Entry(root)
entry_key_normal.pack()

btn_encrypt_normal = tk.Button(root, text="加密 (普通)", command=encrypt_data_normal)
btn_encrypt_normal.pack()

tk.Label(root, text="输入要解密的8位密文:").pack()
entry_decrypt_ciphertext_normal = tk.Entry(root)
entry_decrypt_ciphertext_normal.pack()

tk.Label(root, text="解密密钥（10位）:").pack()
entry_key_decrypt_normal = tk.Entry(root)
entry_key_decrypt_normal.pack()

btn_decrypt_normal = tk.Button(root, text="解密 (普通)", command=decrypt_data_normal)
btn_decrypt_normal.pack()

# ASCII Encrypt Section
tk.Label(root, text="输入要加密的 ASCII 字符串:").pack()
entry_plaintext_ascii = tk.Entry(root)
entry_plaintext_ascii.pack()

tk.Label(root, text="密钥（10位）:").pack()
entry_key_ascii = tk.Entry(root)
entry_key_ascii.pack()

btn_encrypt_ascii = tk.Button(root, text="加密 (ASCII)", command=encrypt_data_ascii)
btn_encrypt_ascii.pack()

tk.Label(root, text="输入要解密的 ASCII 字符串:").pack()
entry_decrypt_ciphertext_ascii = tk.Entry(root)
entry_decrypt_ciphertext_ascii.pack()

tk.Label(root, text="解密密钥（10位）:").pack()
entry_key_decrypt_ascii = tk.Entry(root)
entry_key_decrypt_ascii.pack()

btn_decrypt_ascii = tk.Button(root, text="解密 (ASCII)", command=decrypt_data_ascii)
btn_decrypt_ascii.pack()

# Brute Force Attack Section
tk.Label(root, text="输入要进行暴力破解的密文:").pack()
entry_attack_ciphertext = tk.Entry(root)
entry_attack_ciphertext.pack()

btn_attack = tk.Button(root, text="暴力破解", command=perform_brute_force_attack)
btn_attack.pack()

# Collision Detection Section
tk.Label(root, text="输入要检测冲突的数据:").pack()
entry_collision_input = tk.Entry(root)
entry_collision_input.pack()

btn_collision = tk.Button(root, text="检测冲突", command=find_collision_data)
btn_collision.pack()

# Run main loop
root.mainloop()