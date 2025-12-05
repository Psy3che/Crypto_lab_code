# 1. 数论基础算法
# 最大公约数（GCD）计算：gcd函数通过欧几里得算法求解两个整数的最大公约数，
# 并记录计算过程中的中间值（如被除数、商、除数、余数），为后续扩展欧几里得算法
# 提供数据支撑。
# 模逆元求解：inverse函数基于扩展欧几里得算法，计算整数在模某个数下的乘法逆元，
# 若两数不互质则返回 - 1，这是 RSA 等算法中密钥生成的关键步骤。
# 快速幂运算：fast_exponentiation函数实现了二进制快速幂算法，高效计算a^b mod m，
# 解决了大指数幂运算的效率问题，是密码学中幂模运算的核心工具。
# 2. 素性测试
# fermat函数实现了费马素性测试，这是一种概率性素数判定算法。通过随机选取整数验证费马小定理，
# 若测试通过则以指定概率判定数为素数，若失败则确定为合数。该功能为生成大素数
# （如 RSA、Diffie-Hellman 算法的核心参数）提供了基础。
# 3. 原根（生成元）判定
# 除数计算：divisors函数高效求解一个数的所有除数（不含自身），通过遍历至平方根减少计算量，
# 为原根判定提供数据。
# 生成元判定：is_generator函数依据原根的数学定义，通过验证整数对模素数的幂次特性，判定
# 其是否为模素数的生成元。生成元是 Diffie-Hellman 密钥交换、ElGamal 加密等算法的核心参数。
# 4. 密码学协议实现
# Diffie-Hellman 密钥交换（DH_KEX）：实现了经典的 Diffie-Hellman 密钥交换算法，通过公共
# 的生成元与大素数，结合双方私钥计算共享密钥。函数中还包含对生成元有效性、素数合法性的校验，确保协议安全性。
# ElGamal 与 RSA 框架：EL_GAMAL和RSA函数为这两种经典公钥加密算法预留了实现框架，其中 ElGamal
#  基于 Diffie-Hellman 密钥交换扩展，RSA 则依赖大素数分解的数学难题，代码中已明确其核心设计思路
# （如 RSA 的密钥生成、加解密逻辑）。


def gcd(a:int,b:int)->int:
    collected_info=[]
    r = -1
    while r != 0:
        one_line=[a,a//b,b,a%b]
        r=a%b
        a=b
        b=r
        collected_info.append(one_line)
    return a,collected_info[:-1]

def inverse(a:int,m:int)->int: 
    result,table=gcd(m,a)
    # table[line][1] -> a//b
    if result != 1:
        return -1 # if the gcd is not 1, then there is no inverse
    x=0
    y=1
    for row in range(1,len(table)+1):
        prev_x = x
        x = y
        y = prev_x + y*(-1)*table[-row][1]
    return y%m

    '''
    Idea which gave us the above algorithm:
        Lets "solve" inverse(13,101) manually and write out the steps
    ---------------
    x = 0
    y = 1
    for row in range(1,len(table)+1)
    ---------------
    prev_x = x -> prev_x = 0
    x = y -> x = y 
    y = prev_x + y*(-1)*table[-row][1] -> 0 + 1*(-1)*table[-row][1] ->
    ---------------
    prev_x = x
    x = y
    y = prev_x + y*(-1)*table[-row][1]
    ---------------
    prev_x = x
    x = y
    y = prev_x + y*(-1)*table[-row][1]
    '''

   
def fast_exponentiation(a:int,b:int,m:int)->int:
    '''
    Calculates a^b (mod m)
    '''
    b=bin(b)[2:]
    result=1
    for num in b:
        result = (result**2)%m
        if num=='1':
            result = (result*a)%m
    return result

# PRIMALITY TESTS
def fermat(p:int,prob:float)->bool:
    '''
    Returns either that p is NOT a prime (100%) or that p is a prime with
    probability "prob" (e.g. 0.9999999999)
    Idea: if p is actually a prime then for any positive integer a < p,
    a^(p-1) = 1 (mod p). There is a theorem stating that if an element "a"
    passes this test, then the probability increases with 50%
    (e.g: first pass a^(p-1)=1: 50%, second pass b^(p-1)=1: 75%,
    third pass c^(p-1)=1: 87.5%, fourth pass d^(p-1)=1: 93.75%, etc.)
    However if for ANY positive integer x < p, x^(p-1) is NOT 1 mod p, then
    p is NOT a prime with a 100% probability
    '''
    import random
    final_probability=0
    already_chosen=set([])
    # we choose random elements until we get the desired probability
    while final_probability < prob:
        size_of_set = len(already_chosen)
        if size_of_set == p-1: # for e.g. p=7, already_chosen={1,2,3,4,5,6}
            return True # either 100% prime OR strong Fermat-pseudoprime
        while True:
            chosen_element = random.randint(1,p-1)
            if gcd(chosen_element,p) != 1:
                return False
            already_chosen.add(chosen_element)
            if size_of_set != len(already_chosen):
                break
        
        if fast_exponentiation(chosen_element,p-1,p) != 1:
            print(f'Not a prime because of: {chosen_element}')
            return False
        final_probability = final_probability + (1-final_probability)*0.5
    return True




        

def divisors(a:int)->list:
    '''
    Gives us back the divisors of 'a' NOT INCLUDING 'a'
    E.g. divisors(100) -> [1,2,4,5,10,20,25,50]
    'Bad (but working) idea': loop through between 2 and a-1 and try to divide
    'a' with each number -> PROBLEM: still takes m-1 steps
    'Better idea': same as above, but only loop through between 1 and sqrt(a)
    '''
    result=set([1])
    for i in range(2,int(a**0.5)+1):
        if a%i==0:
            result.add(i)
            result.add(a//i)
    return result

def is_generator(a:int,m:int)->bool:
    '''
    Decides if 'a' is a generator mod m, where m is a prime
    Idea (not efficient): calculate a^1,a^2,...,a^(m-1) (mod m)
    and see if the result is congruent to 1 (mod m).
    If the current power (which gives us 1) is m-1 -> 'a' is a generator
    If the current power (which gives us 1) is LOWER than m-1 -> 'a' is NOT a gen.
    E.g. is_generator(2,7). Here we get that 2^3 (mod 7) is 1, but
    3 is LOWER than 7-1, so 2 is NOT a generator
    But: is_generator(3,7):
    3^1 = 3, 3^2 = 2, 3^3 = 6, 3^4 = 4, 3^5 = 5, 3^6 = 1
    Since the FIRST power which gives us 1 is 6 (7-1), then 3 IS a generator mod 7

    Idea (efficient): loop through only the divisors of phi(m), which m-1, since
    in cryptography we always work with primes, so m is a prime
    '''
    GCD,placeholder = gcd(a,m) # remember, that gcd(a,m) gives back 2 values: GCD, list (used in the inverse)
    if GCD != 1:
        return False

    
    divisors_of_phi_m=divisors(m-1)
    #print(f"Now we are only looping through: {divisors_of_phi_m}")
    for power in divisors_of_phi_m: 
        if fast_exponentiation(a,power,m)==1:
            return False
    return True

def DH_KEX(g:int,p:int,x:int,y:int)->int:
    '''
    Idea: key = (g^x)^y = (g^y)^x = g^(xy)  (mod p)
        Public info: g(enerator), p(rime)
        Private info: Alice -> x, Bob -> y
        Constraints: 1 < g < p, 0 <= x,y <= phi(p) = p-1
            We can assume that these constraints are met
    '''
    if is_generator(g,p) == False:
        return -1
    if fermat(p,0.99999) == False:
        return -1
    return fast_exponentiation(g,x*y,p)

def EL_GAMAL():
    # do the DH ey exchange, then multiply the KEY with the MESSAGE mod p
    # k*m = c (mod p)
    # for decryption: m = c*(k^-1) (mod p)  
    pass

def RSA():
    '''
    p,q primes (secret)
    n = p*q (public)
    random 1<e<phi(n), gcd(e,n)=1, gcd(e,phi(n))=1
    encryption: c=m^e (mod n)
    decryption: find d such that c^d = m, but c^d = m^(e*d), so we need a d
    such that e*d=1 mod (phi(n)), so we need the inverse of e mod phi(n)
    '''
    pass

# ...


def main():
    print(is_generator(3,7))
        
if __name__=="__main__":
    main()






    
