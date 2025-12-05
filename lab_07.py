# 1. 核心数论运算实现
# 最大公约数（GCD）计算：gcd函数基于欧几里得算法，不仅求解两个整数的最大公约数，
# 还通过列表collected_info记录计算过程中的被除数、商、除数、余数等中间数据，
# 为模逆元求解提供底层数据支撑。
# 模逆元求解：inverse函数借助扩展欧几里得算法的思想，利用gcd函数输出的中间数据，
# 计算整数在模某个数下的乘法逆元；若两数不互质（GCD 不为 1），则返回 - 1 表示逆元
# 不存在，这是 RSA 等公钥密码算法中密钥生成的关键步骤。
# 快速幂运算：fast_exponentiation函数实现二进制快速幂算法，高效完成a^b mod m的
# 计算，解决了大指数幂模运算的效率问题，是密码学中幂运算的核心工具，广泛应用于加密、签名验证等场景。
# 2. 素性测试与生成元判定
# 费马素性测试：fermat函数实现概率性的费马素性测试，通过随机选取整数验证费马小定理，
# 逐步提升判定为素数的概率至指定阈值；若测试失败则直接判定为合数，为生成大素数
# （如 RSA、Diffie-Hellman 算法的核心参数）提供基础。
# 除数计算：divisors函数通过遍历至目标数的平方根，高效求解其所有真除数（不含自身），
# 减少了计算量，为生成元判定提供数据支持。
# 模素数生成元判定：is_generator函数依据原根的数学定义，通过验证整数对模素数的幂次特性
# （仅当整数的幂次为模的欧拉函数值时才余 1），判定其是否为模素数的生成元；生成元是
#  Diffie-Hellman 密钥交换、ElGamal 加密等算法的核心参数。
# 3. 密码学协议与算法框架
# Diffie-Hellman 密钥交换（DH_KEX）：实现经典的 Diffie-Hellman 密钥交换算法，
# 通过公共的生成元与大素数，结合双方私钥计算共享密钥；函数内还包含对生成元有效性、
# 素数合法性的校验，确保协议的安全性与正确性。
# 公钥加密算法框架：EL_GAMAL和RSA函数为 ElGamal 加密、RSA 加密这两种经典公钥密码
# 算法预留了实现框架，明确了算法的设计方向，便于后续完善具体的加解密、密钥生成逻辑。



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
    if gcd(a,m) != 1:
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
    pass

def RSA():
    pass


def main():
    print(fermat(341,0.9999))

if __name__=="__main__":
    main()
