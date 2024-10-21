import tkinter as tk
from tkinter import messagebox
from SDES import SDES  # 确保 SDES 类在 sdes.py 中实现
from attack import brute_force_attack  # 确保暴力破解在 attack.py 中实现


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

        # 将每个字符转换为8位二进制并进行加密
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

        # 将密文位转换回ASCII字符串
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

        # 将ASCII字符串转换为二进制数组
        ciphertext_bits = string_to_bit_array(ciphertext)
        decrypted_bits = []

        sdes = SDES(key)

        for i in range(0, len(ciphertext_bits), 8):
            block = ciphertext_bits[i:i + 8]
            if len(block) < 8:
                continue
            decrypted_block = sdes.decrypt(block)
            decrypted_bits.extend(decrypted_block)

        # 将解密后的位转换回ASCII字符串
        decrypted_str = bit_array_to_string(decrypted_bits)
        print(f"解密密文（ASCII）: {ciphertext} -> 明文: {decrypted_str}")
        messagebox.showinfo("解密明文", "解密明文: " + decrypted_str)

    except Exception as e:
        messagebox.showerror("错误", str(e))


def perform_brute_force_attack():
    try:
        plaintext = entry_attack_plaintext.get().strip()
        ciphertext = entry_attack_ciphertext.get().strip()

        if len(plaintext) != 8 or len(ciphertext) != 8:
            raise ValueError("明文和密文必须是8位。")

        # 转换为位数组
        plaintext_bits = list(map(int, plaintext))
        ciphertext_bits = list(map(int, ciphertext))

        # 开始暴力破解
        keys_found, duration = brute_force_attack(plaintext_bits, ciphertext_bits)

        if keys_found:
            result = '\n'.join([''.join(map(str, key)) for key in keys_found])
            messagebox.showinfo("暴力破解结果", f"找到的密钥:\n{result}\n消耗时间: {duration:.9f}秒")

        else:
            messagebox.showinfo("暴力破解结果", "没有找到合适的密钥。")

    except Exception as e:
        messagebox.showerror("错误", str(e))


# GUI 设置
root = tk.Tk()
root.title("S-DES 和 ASCII 转换器")

# 普通加密功能部分
tk.Label(root, text="输入明文（8位）:").pack()
entry_plaintext_normal = tk.Entry(root)
entry_plaintext_normal.pack()

tk.Label(root, text="输入密钥（10位）:").pack()
entry_key_normal = tk.Entry(root)
entry_key_normal.pack()

btn_encrypt_normal = tk.Button(root, text="普通加密", command=encrypt_data_normal)
btn_encrypt_normal.pack()

# 普通解密功能部分
tk.Label(root, text="输入密文（8位）:").pack()
entry_decrypt_ciphertext_normal = tk.Entry(root)
entry_decrypt_ciphertext_normal.pack()

tk.Label(root, text="输入密钥（10位）:").pack()
entry_key_decrypt_normal = tk.Entry(root)
entry_key_decrypt_normal.pack()

btn_decrypt_normal = tk.Button(root, text="普通解密", command=decrypt_data_normal)
btn_decrypt_normal.pack()

# ASCII 加密功能部分
tk.Label(root, text="输入ASCII明文:").pack()
entry_plaintext_ascii = tk.Entry(root)
entry_plaintext_ascii.pack()

tk.Label(root, text="输入密钥（10位）:").pack()
entry_key_ascii = tk.Entry(root)
entry_key_ascii.pack()

btn_encrypt_ascii = tk.Button(root, text="ASCII加密", command=encrypt_data_ascii)
btn_encrypt_ascii.pack()

# ASCII 解密功能部分
tk.Label(root, text="输入ASCII密文:").pack()
entry_decrypt_ciphertext_ascii = tk.Entry(root)
entry_decrypt_ciphertext_ascii.pack()

tk.Label(root, text="输入密钥（10位）:").pack()
entry_key_decrypt_ascii = tk.Entry(root)
entry_key_decrypt_ascii.pack()

btn_decrypt_ascii = tk.Button(root, text="ASCII解密", command=decrypt_data_ascii)
btn_decrypt_ascii.pack()

# 暴力破解功能部分
tk.Label(root, text="输入明文（8位）:").pack()
entry_attack_plaintext = tk.Entry(root)
entry_attack_plaintext.pack()

tk.Label(root, text="输入密文（8位）:").pack()
entry_attack_ciphertext = tk.Entry(root)
entry_attack_ciphertext.pack()

btn_brute_force = tk.Button(root, text="执行暴力破解", command=perform_brute_force_attack)
btn_brute_force.pack()

root.mainloop()