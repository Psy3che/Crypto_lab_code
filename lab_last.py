# 1. 维吉尼亚加密功能
# vigenere_cipher函数接收明文数字列表message和密钥数字列表key作为参数，通过循环遍历明文
# 中的每个数字，将其与密钥中对应位置的数字（密钥按长度循环复用，即通过i%len(key)实现密钥的
# 循环选取）相加后对 26 取模，得到加密后的数字，并将所有加密结果存入列表返回，完成维吉尼亚密码的加密过程。
# 2. 维吉尼亚解密功能（存在逻辑缺陷）
# vigenere_decipher函数意图实现维吉尼亚密码的解密逻辑，设计思路为将密文数字与密钥数字（同样循环复用）
# 相减后加 26 再对 26 取模（避免负数结果），但函数内部存在明显的逻辑错误：函数开头将传入的message参数
# 重新赋值为空列表，导致后续循环无法遍历密文数据，实际无法完成解密操作，仅为功能框架的初步构建。
def vigenere_cipher(message, key):
   cipher=[]
   for i in range (0,len(message)):
      cipher.append((message[i]+key[i%len(key)])%26)
   return cipher
def vigenere_decipher(message, key):
    message=[]
    for i in range (0,len(message)):
        message.append((message[i]-key[i%len(key)]+26)%26)
    return message
    
def main():
    # 使用Vigenère密码加密数字列表，参数分别为明文和密钥
    result=vigenere_cipher([0,15,15,11,4], [3,14,6])
    print(result)
if __name__=='__main__':
    main()
