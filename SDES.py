class SDES:
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
    EP_BOX = [4, 1, 2, 3, 2, 3, 4, 1]
    S_BOX_1 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 0, 2],
    ]
    S_BOX_2 = [
        [0, 1, 2, 3],
        [2, 3, 1, 0],
        [3, 0, 1, 2],
        [2, 1, 0, 3],
    ]
    SP_BOX = [2, 4, 3, 1]

    def __init__(self, key):
        self.key = key
        self.k1, self.k2 = self.key_expansion()

    def key_expansion(self):
        # Permute key using P10
        permuted_key = self.permute(self.key, self.P10)
        left, right = permuted_key[:5], permuted_key[5:]

        # Shift left for k1
        left_shifted_1 = left[1:] + left[:1]
        right_shifted_1 = right[1:] + right[:1]
        k1 = self.permute(left_shifted_1 + right_shifted_1, self.P8)

        # Shift left for k2
        left_shifted_2 = left[2:] + left[:2]
        right_shifted_2 = right[2:] + right[:2]
        k2 = self.permute(left_shifted_2 + left_shifted_2, self.P8)

        return k1, k2

    @staticmethod
    def permute(bits, permutation):
        return [bits[i - 1] for i in permutation]

    @staticmethod
    def shift(bits, n):
        return bits[n:] + bits[:n]

    def f(self, right, k):
        # Expand and permute
        expanded = self.permute(right, self.EP_BOX)

        # XOR with key
        xor_result = [expanded[i] ^ k[i] for i in range(8)]

        # Split into two 4-bit halves
        left, right = xor_result[:4], xor_result[4:]

        # S-Boxes
        row1 = (left[0] << 1) + left[3]
        col1 = (left[1] << 1) + left[2]
        s_box_output1 = self.S_BOX_1[row1][col1]

        row2 = (right[0] << 1) + right[3]
        col2 = (right[1] << 1) + right[2]
        s_box_output2 = self.S_BOX_2[row2][col2]

        # Combine S-Box outputs
        combined = [int(b) for b in f"{s_box_output1:02b}" + f"{s_box_output2:02b}"]

        # Final permutation
        return self.permute(combined, self.SP_BOX)

    def encrypt(self, plaintext):
        # Initial permutation
        permuted = self.permute(plaintext, self.IP)

        # Split into two halves
        left, right = permuted[:4], permuted[4:]

        # Round 1
        right_f1 = self.f(right, self.k1)
        left = [left[i] ^ right_f1[i] for i in range(4)]

        # Swap
        left, right = right, left

        # Round 2
        right_f2 = self.f(right, self.k2)
        left = [left[i] ^ right_f2[i] for i in range(4)]

        # Final permutation
        return self.permute(left + right, self.IP_INV)

    def decrypt(self, ciphertext):
        # Initial permutation
        permuted = self.permute(ciphertext, self.IP)

        # Split into two halves
        left, right = permuted[:4], permuted[4:]

        # Round 1
        right_f2 = self.f(right, self.k2)
        left = [left[i] ^ right_f2[i] for i in range(4)]

        # Swap
        left, right = right, left

        # Round 2
        right_f1 = self.f(right, self.k1)
        left = [left[i] ^ right_f1[i] for i in range(4)]

        # Final permutation
        return self.permute(left + right, self.IP_INV)