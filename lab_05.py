# 1. 快速幂运算实现
# fast_exponentiation函数实现了二进制快速幂算法，专门用于高效计算a^b mod m的值。
# 该算法通过将指数b转换为二进制形式，逐位处理并结合平方取模操作，大幅降低了大指数幂模
# 运算的时间复杂度，是密码学中加密、签名验证等操作的核心基础工具。
# 2. 除数求解函数（存在逻辑偏差）
# divisors函数设计目标是求解一个数的所有除数，但实际实现逻辑为质因数分解（通过遍历
# 除数并不断整除目标数，收集质因数），与注释中描述的 “返回所有除数” 功能存在偏差。尽管
# 如此，该函数仍尝试通过优化遍历方式（虽实际未按平方根优化执行）减少计算量，为后续数论
# 操作提供数据支撑。
# 3. 模素数生成元判定（基础实现）
# is_generator函数实现了模素数生成元的判定逻辑，其核心思路为：遍历 1 到m-2的幂次
# ，验证整数a的幂次取模m是否为 1，若存在小于m-1的幂次满足条件，则判定a非生成元，否
# 则为生成元。该实现为基础的暴力验证方式，虽未采用优化的除数遍历策略，但完整体现了生
# 成元判定的核心数学原理，是 Diffie-Hellman 密钥交换、ElGamal 加密等算法中参数选
# 择的关键步骤。
def gcd(a:int,b:int)->int:
    pass

def inverse(a:int,m:int)->int: 
    pass

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

def divisors(a:int)->list:
    '''
    Gives us back the divisors of 'a'
    E.g. divisors(100) -> [1,2,4,5,10,20,25,50,100]
    'Bad (but working) idea': loop through between 2 and a-1 and try to divide
    'a' with each number -> PROBLEM: still takes m-1 steps
    'Better idea': same as above, but only loop through between 1 and sqrt(a)
    '''
    result=[1]
    divisor=2
    while a != 1:
        if a%divisor == 0:
            a = a//divisor
            result.append(divisor)
        divisor = divisor+1
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
    '''
    for power in range(1,m-1): 
        if fast_exponentiation(a,power,m)==1:
            return False
    return True


def main():
    print(divisors(100))
    #59428043 -> is_generator was not able to decide, since it is a 'large' num

if __name__=="__main__":
    main()
