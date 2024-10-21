# ASCII.py

def string_to_byte_array(text):
    """Convert ASCII string to a byte array (list of bits)."""
    byte_array = []
    for char in text:
        bits = bin(ord(char))[2:].zfill(8)  # Convert to binary and pad to 8 bits
        byte_array.extend(int(bit) for bit in bits)  # Add bits to the array
    return byte_array

def byte_array_to_string(byte_array):
    """Convert a byte array (list of bits) back to ASCII string."""
    chars = []
    for i in range(0, len(byte_array), 8):
        byte = byte_array[i:i+8]
        if len(byte) < 8:
            break  # Skip incomplete bytes
        char = chr(int(''.join(map(str, byte)), 2))  # Convert bits back to a char
        chars.append(char)
    return ''.join(chars)