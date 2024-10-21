# 作业1：S-DES算法实现
## 1、作业任务:
根据"信息安全导论"课程第5次课讲述的S-DES算法，使用你们自己最擅长的程序语言(C++/QT或Java+Swing、Python+QT等)来编程实现加、解密程序。

本人使用Python+QT

##  2、标准设定
参考[作业1：S-DES算法实现]([作业1：S-DES算法实现](https://shimo.im/docs/m5kvdlMaKvcENy3X?fallback=1))

## 3、编程和测试要求
### 第一关    基本测试
定义一个SDES.py文件，主要用于实现基本的加密解密过程

**类定义及常量**
```python
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
```
**构造函数**
```python
def __init__(self, key):
    self.key = key
    self.k1, self.k2 = self.key_expansion()
```
**密钥扩展**
```python
def key_expansion(self):
    permuted_key = self.permute(self.key, self.P10)
    left, right = permuted_key[:5], permuted_key[5:]

    left_shifted_1 = left[1:] + left[:1]
    right_shifted_1 = right[1:] + right[:1]
    k1 = self.permute(left_shifted_1 + right_shifted_1, self.P8)

    left_shifted_2 = left[2:] + left[:2]
    right_shifted_2 = right[2:] + right[:2]
    k2 = self.permute(left_shifted_2 + left_shifted_2, self.P8)

    return k1, k2
```
**加密函数**
```python
def f(self, right, k):
    # Expand and permute
    expanded = self.permute(right, self.EP_BOX)

    xor_result = [expanded[i] ^ k[i] for i in range(8)]

    left, right = xor_result[:4], xor_result[4:]

    row1 = (left[0] << 1) + left[3]
    col1 = (left[1] << 1) + left[2]
    s_box_output1 = self.S_BOX_1[row1][col1]

    row2 = (right[0] << 1) + right[3]
    col2 = (right[1] << 1) + right[2]
    s_box_output2 = self.S_BOX_2[row2][col2]

    combined = [int(b) for b in f"{s_box_output1:02b}" + f"{s_box_output2:02b}"]

    return self.permute(combined, self.SP_BOX)
```
**解密函数**
```python
def decrypt(self, ciphertext):
    permuted = self.permute(ciphertext, self.IP)

    left, right = permuted[:4], permuted[4:]

    right_f2 = self.f(right, self.k2)
    left = [left[i] ^ right_f2[i] for i in range(4)]

    left, right = right, left

    right_f1 = self.f(right, self.k1)
    left = [left[i] ^ right_f1[i] for i in range(4)]

    return self.permute(left + right, self.IP_INV)
```
在GUI窗口中实现了基础的加解密过程，先后输入8bit的明文和10bit的密钥，点击解密按钮，即可跳出弹窗生成对应密文；先后输入8bit的密文和10bit的密钥，即可跳出弹窗生成对应明文。同时后台会打印出生成的密文和明文。
![GUI互动平面](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185046.png)

![输入明文密钥](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185216.png)

![加密结果](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185224.png)

![解密结果](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185234.png)

![后台打印加密解密结果](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185316.png)

### 第二关    交叉测试
明文：11111111
密钥：1111111111
对比张婷组的加密情况如下：
![张婷组加密结果与本组一致](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185332.png)
密文：11111110
密钥：1111111111
对比涨停组的解密情况如下：
![张婷组解密结果与本组一致](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185340.png)

### 第三关    扩展功能
考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为1 Byte)，对应地输出也可以是ACII字符串(很可能是乱码)。

**ASCII加解密**
```python
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
            break # Skip incomplete bytes  
  char = chr(int(''.join(map(str, byte)), 2))  # Convert bits back to a char  
  chars.append(char)  
    return ''.join(chars)
```
输入的ASCII明文：abandon，密钥：1111111111，结果如下：
![ASCII加密](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185241.png)

输入的ASCII密文：SãS，密钥：1111111111，结果如下：、
![ASCII解密](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185256.png)

### 第四关    暴力破解
假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用暴力破解的方法找到正确的密钥Key。在编写程序时，你也可以考虑使用多线程的方式提升破解的效率。请设定时间戳，用视频或动图展示你在多长时间内完成了暴力破解。

-   方法分析：  
    知道一对或多对明密文对，且知道密钥为10bit二进制，因此一共有1024种密钥情况。采用多线程遍历的方法暴力求解。
-   性能分析：  
    为了第五关的测试、我们要遍历所有的密钥、因此中途不停止搜索。记录开始破解到找到第一个密钥的时间、即为破解时间。
-   测试：
      ![暴力破解结果](https://github.com/Braevi/-/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-10-21%20185306.png)
